"""
Pipeline workflow to retrain models on data.
This file has a whole range of functions that represent tasks in a MLOps retraining process
"""

import argparse
import typing as t
from pathlib import Path

import polars as pl
from box import Box
from prefect import flow, get_run_logger, task
from prefect.utilities.annotations import quote
from src.data import DataEngine, TransformerOutput
from src.model import LearnLab, TunerOutput
from src.utils import Pilot
from src.visualize import Vizard


@task(
    name="setup_pipeline",
    description="Setup directories and logging for the pipeline experiment",
)
def setup_pipeline(
    config_filepath: str,
) -> t.Tuple[
    Box,
    Path,
    Path,
    Path,
    Path,
]:
    """
    Creates directories and sets random seed for reproducibility
    """
    return Pilot.setup(filepath=config_filepath)


@task(
    name="data_loader",
    description="Load your data here and return one single dataframe",
    retries=3,
    retry_delay_seconds=3,
)
def data_loader(config: Box) -> pl.DataFrame:
    """
    Loads data
    """
    return DataEngine.load(config.data.load)


@task(name="data_validator", description="Validate data to fit the schema")
def data_validator(data) -> pl.DataFrame:
    """
    Validates data
    """
    return DataEngine.validate(data)


@task(
    name="data_split",
    description="Split data into training and test sets",
)
def data_splits(
    config: Box,
    data: pl.DataFrame,
) -> t.Tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame, pl.DataFrame]:
    """
    Splits the data into train and test sets
    """
    return DataEngine.split(config.data.split, data=data, seed=config.SEED)


@task(
    name="data_transformer",
    description="Transform data into numerical encoding using preprocessors",
)
def data_transformer(
    config: Box,
    X_train: pl.DataFrame,
    X_test: pl.DataFrame,
    y_train: pl.DataFrame,
    y_test: pl.DataFrame,
    artifact_dir: Path,
) -> TransformerOutput:
    """
    Applies transformation like scaling and encoding to data
    """
    return DataEngine.transform(
        config=config.data.transform,
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
        artifact_dir=artifact_dir,
    )


@task(
    name="train_models",
    description="Trains model based on params, returns a dataframe containing metrics",
)
def train_models(
    config: Box, transformed_ds: t.Type[TransformerOutput]
) -> pl.DataFrame:
    """
    Trains models based on configuration
    """
    return LearnLab.train_experiments(
        config=config.model.train, transformed_ds=transformed_ds
    )


@task(
    name="tune_models",
    description="Tunes models based on params, returns a TunerObject",
)
def tune_models(
    config: Box, transformed_ds: t.Type[TransformerOutput], model_dir: Path
) -> TunerOutput:
    """
    Tunes models based on configuration
    """
    return LearnLab.tune_models(
        config=config.model.tune, transformed_ds=transformed_ds, model_dir=model_dir
    )


@task(
    name="make_plots_and_viz",
    description="Create visualizations for model explainability and data analysis",
    retries=2,
)
def visualize_insights(**kwargs) -> None:
    """
    Creates plots and visualizations for data analysis, results of training and hyper-parameter tuning
    """
    if kwargs.get("data") is not None and kwargs.get("viz_dir") is not None:
        Vizard.plot_target_dist(data=kwargs.get("data"), viz_dir=kwargs.get("viz_dir"))
    if kwargs.get("data") is not None and kwargs.get("viz_dir") is not None:
        Vizard.plot_cust_info(data=kwargs.get("data"), viz_dir=kwargs.get("viz_dir"))
    if kwargs.get("data") is not None and kwargs.get("viz_dir") is not None:
        Vizard.plot_num_dist(data=kwargs.get("data"), viz_dir=kwargs.get("viz_dir"))
    if kwargs.get("results") is not None and kwargs.get("viz_dir") is not None:
        Vizard.plot_training_results(
            results=kwargs.get("results"), viz_dir=kwargs.get("viz_dir")
        )
    if kwargs.get("tuner") is not None and kwargs.get("viz_dir") is not None:
        Vizard.plot_optuna_study(
            study=kwargs.get("tuner").studies[0], viz_dir=kwargs.get("viz_dir")
        )
    return None


# FIXME
@task(
    name="push_artifacts",
    description="Push artifacts to W&B server and Prefect server",
    retries=3,
    retry_delay_seconds=3,
)
def push_artifacts(tuner: TunerOutput, viz_dir: Path, artifact_dir: Path) -> None:
    """
    Pushes various artifacts such as log files, visualizations and models to respective servers and storage spaces
    """
    return Pilot.push_artifacts(tuner=tuner, viz_dir=viz_dir, artifact_dir=artifact_dir)


@flow(
    name="Churnobyl_retraining_pipeline_workflow",
    description="Pipeline for automated ml workflow",
)
def workflow(config_path: str) -> None:
    """
    Entire pipeline, uses native Python logging

    Args:
        config_path (Path): Path for config file
    """
    logger = get_run_logger()

    (
        config,
        ROOT_DIR,
        viz_dir,
        model_dir,
        artifact_dir,
    ) = setup_pipeline(config_filepath=config_path)
    logger.info("Setup has been configured")

    data = data_loader(config=config)
    logger.info("Data has been loaded")

    X_train, X_test, y_train, y_test = data_splits(config=config, data=data)
    logger.info("Data splits have been made")

    transformed_ds = data_transformer(
        config=config,
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
        artifact_dir=artifact_dir,
    )
    logger.info("Data transformers have been applied")

    results = train_models(config=config, transformed_ds=transformed_ds)
    tuner = tune_models(
        config=config, transformed_ds=transformed_ds, model_dir=model_dir
    )
    logger.info("Best model has been acquired")

    visualize_insights(
        data=data,
        results=results,
        tuner=quote(tuner),
        viz_dir=viz_dir,
    )
    logger.info("Visualizations have been drawn")

    push_artifacts(tuner=quote(tuner), viz_dir=viz_dir, artifact_dir=artifact_dir)
    logger.info("Artifacts have been uploaded to remote destination")


if __name__ == "__main__":
    # assert (
    #     Path.cwd().stem == "churninator"
    # ), "Run code from 'churninator', not from `churnobyl`"
    parser = argparse.ArgumentParser(
        prog="Churnobyl-69420",
        description="For config file only",
    )
    parser.add_argument("--config", default="./churnobyl/conf/config.yaml")
    args = parser.parse_args()
    workflow(config_path=args.config)
