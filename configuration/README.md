# 📑 configuration/README.md

## Experiment Settings

This directory contains experiment configuration files (`.ini`) and the logic to load them (`DIConfiguration.py`).  
Each `.ini` file corresponds to a distinct experiment scenario described in the paper (<paper url>).  
By changing the `.ini` file referenced in `DIConfiguration.py` (`configFilePath = "XXXX.ini"`), you can reproduce different experiments.

---

### 📂 Files

- **`*.ini`**  
  Defines experiment parameters (e.g., LLM service, text generation service, whether to use error feedback).  
  Each `.ini` represents one reproducible experiment setup.

- **`DIConfiguration.py`**  
  Responsible for selecting and loading the correct `.ini` file.  
  Typically controlled by:
  ```python
  configFilePath = "exp1.ini"
  ```
---

### ⚙️ Config Structure

A typical .ini file contains the following sections:
  ```ini
    [Global]
    # General experiment settings
    episode_step = 16

    [Environment]
    llm_service = RLEnvForApp.adapter.llmService.GeminiService.GeminiService
    observation_service = RLEnvForApp.domain.environment.observationService.DefaultForTestObservationService.DefaultForTestObservationService
    action_command_factory = RLEnvForApp.domain.environment.actionCommandFactoryService.LLMActionCommandFactory.LLMActionCommandFactory
    reward_calculator_service = RLEnvForApp.domain.environment.rewardCalculatorService.VerifyPhaseRewardCalculatorService.VerifyPhaseRewardCalculatorService

    target_page_repository = RLEnvForApp.adapter.repository.targetPage.InMemoryTargetPageRepository.InMemoryTargetPageRepository
    episode_handler_repository = RLEnvForApp.adapter.repository.episodeHandler.InMemoryEpisodeHandlerRepository.InMemoryEpisodeHandlerRepository
    application_under_test_repository = RLEnvForApp.adapter.repository.applicationUnderTest.InMemoryApplicationUnderTestRepository.InMemoryApplicationUnderTestRepository

    episode_handler = RLEnvForApp.domain.environment.episodeHandler.AIGuideNoCoverageEpisodeHandler.AIGuideNoCoverageEpisodeHandler
    application_handler = RLEnvForApp.adapter.applicationUnderTest.DockerServerHandler.DockerServerHandler
    target_page_queue_manager = RLEnvForApp.usecase.targetPage.queueManager.GUIDETargetPageQueueManagerService.GUIDETargetPageQueueManagerService
    directive_rule_service = RLEnvForApp.domain.targetPage.DirectiveRuleService.LLMBasedDirectiveRuleService.LLMBasedDirectiveRuleService
    field_rule_service = RLEnvForApp.domain.targetPage.FieldRuleService.RequiredFieldRuleService.RequiredFieldRuleService
    feedback_rule_service = RLEnvForApp.domain.targetPage.FeedbackRuleService.FormFieldFeedbackRuleService.FormFieldFeedbackRuleService

    [Agent]
    cnn_extractor = RLEnvForApp.adapter.agent.policy.extractor.MorePagesExperimentExtractor.MorePagesExperimentExtractor.getExtractor
    environment = RLEnvForApp.adapter.environment.gym.AIGuideEnvironment.AIGuideEnvironment

    [InputGeneration]
    # Input/text generation strategy
    text_generation_service = RLEnvForApp.adapter.formInput.textGeneration.MixedTextGenerationService.MixedTextGenerationService

    [BERT]
    bert_official = True
    bert_model_name = BERT-Tiny
    bert_model_dir = model/bert

  ```

### 📊 Current Experiment Configurations

file name                           | exp  | llm service      | check required field | feedback enabled | text generation    | form success judge
------------------------------------|------|------------------|----------------------|-----------------|-------------------|-------------------
LLM_exp_fill_all_field.ini          | exp1 | Gemini 2.0 Flash | no                   | enable          | Mixed             | only LLM
LLM_exp_check_field_required.ini    | exp1 | Gemini 2.0 Flash | yes                  | enable          | Mixed             | only LLM
LLM_exp_feedback_disabled.ini       | exp2 | Gemini 2.0 Flash | no                   | disable         | LLM               | only LLM
LLM_exp_check_field_required.ini    | exp2 | Gemini 2.0 Flash | no                   | enable          | LLM               | only LLM
LLM_exp_input_datafaker_select.ini  | exp3 | Gemini 2.0 Flash | no                   | enable          | DatafakerSelector | only LLM
LLM_exp_input_llm_only.ini          | exp3 | Gemini 2.0 Flash | no                   | enable          | LLM               | only LLM
LLM_exp_input_mixed.ini             | exp3 | Gemini 2.0 Flash | no                   | enable          | Mixed             | only LLM
LLM_exp_page_compare_assisted.ini   | —    | Gemini 2.0 Flash | yes                  | enable          | LLM               | similarity + LLM
LLM_exp_page_compare_llm_only.ini   | —    | Gemini 2.0 Flash | yes                  | enable          | LLM               | only LLM
LLM_exp_GeminiPro.ini               | —    | Gemini 2.5 Pro   | yes                  | enable          | Mixed             | only LLM
