# Copyright 2024 DataRobot, Inc. and its affiliates.
# All rights reserved.
# DataRobot, Inc.
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
# Released under the terms of DataRobot Tool and Utility Agreement.

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import datarobot as dr
import pulumi_datarobot as datarobot
from datarobot.enums import VectorDatabaseChunkingMethod, VectorDatabaseEmbeddingModel
from pydantic import BaseModel, ConfigDict, Field

from forecastic.schema import FeatureSettingConfig

from .globals import (
    GlobalGuardrailTemplateName,
    GlobalLLM,
    GlobalPredictionEnvironmentPlatforms,
)


class Stage(str, Enum):
    PROMPT = "prompt"
    RESPONSE = "response"


class ModerationAction(str, Enum):
    BLOCK = "block"
    REPORT = "report"
    REPORT_AND_BLOCK = "reportAndBlock"


class GuardConditionComparator(Enum):
    """The comparator used in a guard condition."""

    GREATER_THAN = "greaterThan"
    LESS_THAN = "lessThan"
    EQUALS = "equals"
    NOT_EQUALS = "notEquals"
    IS = "is"
    IS_NOT = "isNot"
    MATCHES = "matches"
    DOES_NOT_MATCH = "doesNotMatch"
    CONTAINS = "contains"
    DOES_NOT_CONTAIN = "doesNotContain"


class Condition(BaseModel):
    comparand: float | str | bool | list[str]
    comparator: GuardConditionComparator


class Intervention(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    action: ModerationAction
    condition: Condition
    message: str
    # send_notification: bool


class GuardrailTemplate(BaseModel):
    template_name: str
    registered_model_name: Optional[str] = None
    name: str
    stages: list[Stage]
    intervention: Intervention


# datarobot.CustomModelArgs()


class CustomModelArgs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    resource_name: str
    name: str
    description: str | None = None
    base_environment_id: str
    base_environment_name: str
    base_environment_version_id: str | None = None
    target_name: str | None = None
    target_type: str | None = None
    runtime_parameter_values: (
        list[datarobot.CustomModelRuntimeParameterValueArgs] | None
    ) = None
    files: list[tuple[str, str]] | None = None
    class_labels: list[str] | None = None
    negative_class_label: str | None = None
    positive_class_label: str | None = None
    folder_path: str | None = None


class RegisteredModelArgs(BaseModel):
    resource_name: str
    name: str


class DeploymentArgs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    resource_name: str
    label: str
    association_id_settings: datarobot.DeploymentAssociationIdSettingsArgs | None = None
    bias_and_fairness_settings: (
        datarobot.DeploymentBiasAndFairnessSettingsArgs | None
    ) = None
    challenger_models_settings: (
        datarobot.DeploymentChallengerModelsSettingsArgs | None
    ) = None
    challenger_replay_settings: (
        datarobot.DeploymentChallengerReplaySettingsArgs | None
    ) = None
    drift_tracking_settings: datarobot.DeploymentDriftTrackingSettingsArgs | None = None
    health_settings: datarobot.DeploymentHealthSettingsArgs | None = None
    importance: str | None = None
    prediction_intervals_settings: (
        datarobot.DeploymentPredictionIntervalsSettingsArgs | None
    ) = None
    prediction_warning_settings: (
        datarobot.DeploymentPredictionWarningSettingsArgs | None
    ) = None
    predictions_by_forecast_date_settings: (
        datarobot.DeploymentPredictionsByForecastDateSettingsArgs | None
    ) = None
    predictions_data_collection_settings: (
        datarobot.DeploymentPredictionsDataCollectionSettingsArgs | None
    ) = None
    predictions_settings: datarobot.DeploymentPredictionsSettingsArgs | None = None
    segment_analysis_settings: (
        datarobot.DeploymentSegmentAnalysisSettingsArgs | None
    ) = None


class CustomModelGuardConfigurationArgs(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    stages: list[Stage]
    template_name: GlobalGuardrailTemplateName
    intervention: Intervention
    input_column_name: str | None = None
    output_column_name: str | None = None


class PlaygroundArgs(BaseModel):
    resource_name: str
    name: str


class LLMSettings(BaseModel):
    max_completion_length: int = Field(le=512)
    system_prompt: str


class VectorDatabaseSettings(BaseModel):
    max_documents_retrieved_per_prompt: Optional[int] = None
    max_tokens: Optional[int] = None


class LLMBlueprintArgs(BaseModel):
    resource_name: str
    name: str
    llm_settings: LLMSettings
    llm_id: GlobalLLM
    vector_database_settings: VectorDatabaseSettings


class ChunkingParameters(BaseModel):
    embedding_model: VectorDatabaseEmbeddingModel | None = None
    chunking_method: VectorDatabaseChunkingMethod | None = None
    chunk_size: int | None = Field(ge=128, le=512)
    chunk_overlap_percentage: int | None = None
    separators: list[str] | None = None


class VectorDatabaseArgs(BaseModel):
    resource_name: str
    name: str
    chunking_parameters: ChunkingParameters


class DatasetArgs(BaseModel):
    resource_name: str
    file_path: str
    name: str


class UseCaseArgs(BaseModel):
    resource_name: str
    name: str
    description: str | None


class PredictionEnvironmentArgs(BaseModel):
    resource_name: str
    name: str
    platform: GlobalPredictionEnvironmentPlatforms


class CredentialArgs(BaseModel):
    resource_name: str
    name: str


class QaApplicationArgs(BaseModel):
    resource_name: str
    name: str


class CalendarArgs(BaseModel):
    name: str
    country_code: str
    start_date: str | datetime
    end_date: str | datetime


class AdvancedOptionsArgs(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    weights: str | None = None
    response_cap: bool | float | None = None
    blueprint_threshold: int | None = None
    seed: int | None = None
    smart_downsampled: bool | None = None
    majority_downsampling_rate: float | None = None
    offset: List[str] | None = None
    exposure: str | None = None
    accuracy_optimized_mb: bool | None = None
    scaleout_modeling_mode: str | None = None
    events_count: str | None = None
    monotonic_increasing_featurelist_id: str | None = None
    monotonic_decreasing_featurelist_id: str | None = None
    only_include_monotonic_blueprints: bool | None = None
    allowed_pairwise_interaction_groups: List[Tuple[str, ...]] | None = None
    blend_best_models: bool | None = None
    scoring_code_only: bool | None = None
    prepare_model_for_deployment: bool | None = None
    consider_blenders_in_recommendation: bool | None = None
    min_secondary_validation_model_count: int | None = None
    shap_only_mode: bool | None = None
    autopilot_data_sampling_method: str | None = None
    run_leakage_removed_feature_list: bool | None = None
    autopilot_with_feature_discovery: bool | None = False
    feature_discovery_supervised_feature_reduction: bool | None = None
    exponentially_weighted_moving_alpha: float | None = None
    external_time_series_baseline_dataset_id: str | None = None
    use_supervised_feature_reduction: bool | None = True
    primary_location_column: str | None = None
    protected_features: List[str] | None = None
    preferable_target_value: str | None = None
    fairness_metrics_set: str | None = None
    fairness_threshold: str | None = None
    bias_mitigation_feature_name: str | None = None
    bias_mitigation_technique: str | None = None
    include_bias_mitigation_feature_as_predictor_variable: bool | None = None
    default_monotonic_increasing_featurelist_id: str | None = None
    default_monotonic_decreasing_featurelist_id: str | None = None
    model_group_id: str | None = None
    model_regime_id: str | None = None
    model_baselines: List[str] | None = None
    incremental_learning_only_mode: bool | None = None
    incremental_learning_on_best_model: bool | None = None
    chunk_definition_id: str | None = None
    incremental_learning_early_stopping_rounds: int | None = None


class DatetimePartitioningArgs(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    datetime_partition_column: str
    autopilot_data_selection_method: str | None = None
    validation_duration: str | None = None
    holdout_start_date: Any | None = None
    holdout_duration: str | None = None
    disable_holdout: bool | None = None
    gap_duration: str | None = None
    number_of_backtests: int | None = None
    backtests: Any | None = None
    use_time_series: bool = False
    default_to_known_in_advance: bool = False
    default_to_do_not_derive: bool = False
    feature_derivation_window_start: int | None = None
    feature_derivation_window_end: int | None = None
    feature_settings: Any | None = None
    forecast_window_start: int | None = None
    forecast_window_end: int | None = None
    windows_basis_unit: str | None = None
    treat_as_exponential: str | None = None
    differencing_method: str | None = None
    periodicities: Any | None = None
    multiseries_id_columns: List[str] | None = None
    use_cross_series_features: bool | None = None
    aggregation_type: str | None = None
    cross_series_group_by_columns: List[str] | None = None
    calendar_id: str | None = None
    holdout_end_date: Any | None = None
    unsupervised_mode: bool = False
    model_splits: int | None = None
    allow_partial_history_time_series_predictions: bool = False
    unsupervised_type: str | None = None


class AnalyzeAndModelArgs(BaseModel):
    target: Any | None = None
    mode: Any = dr.enums.AUTOPILOT_MODE.QUICK
    metric: Any | None = None
    worker_count: Any | None = None
    positive_class: Any | None = None
    partitioning_method: Any | None = None
    featurelist_id: Any | None = None
    advanced_options: Any | None = None
    max_wait: int = dr.enums.DEFAULT_MAX_WAIT
    target_type: Any | None = None
    credentials: Any | None = None
    feature_engineering_prediction_point: Any | None = None
    unsupervised_mode: bool = False
    relationships_configuration_id: Any | None = None
    class_mapping_aggregation_settings: Any | None = None
    segmentation_task_id: Any | None = None
    unsupervised_type: Any | None = None
    autopilot_cluster_list: Any | None = None
    use_gpu: Any | None = None


class AutopilotRunArgs(BaseModel):
    name: str
    create_from_dataset_config: Dict[str, Any] | None = None
    analyze_and_model_config: AnalyzeAndModelArgs | None = None
    datetime_partitioning_config: DatetimePartitioningArgs | None = None
    feature_settings_config: List[FeatureSettingConfig] | None = None
    advanced_options_config: AdvancedOptionsArgs | None = None
    user_defined_segment_id_columns: List[str] | None = None


class ApplicationSourceArgs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    resource_name: str
    files: Optional[Any] = None
    folder_path: Optional[str] = None
    name: Optional[str] = None
    resource_settings: Optional[datarobot.ApplicationSourceResourceSettingsArgs] = None