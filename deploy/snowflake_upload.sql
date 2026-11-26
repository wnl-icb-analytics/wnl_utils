-- Run by .github/workflows/deploy.yml via:
--   snow sql -f deploy/snowflake_upload.sql -D whl_path=<abs path to .whl> -x ...
-- <% whl_path %> is substituted by the Snowflake CLI before execution.

----------------------------------
-- Environment

use role "EXTERNAL_ACCESS_ADMIN";
use secondary roles none;

use schema "EXTERNAL_ACCESS"."WNL-UTILS";

----------------------------------
-- Python File Deployment

create stage if not exists "STG__PYTHON_FILES";

put 'file://<% whl_path %>' '@"STG__PYTHON_FILES"/wnl-utils/'
  auto_compress = FALSE
  overwrite = TRUE
;

grant read on stage "EXTERNAL_ACCESS"."WNL-UTILS"."STG__PYTHON_FILES" to role "ENGINEER";
grant read on stage "EXTERNAL_ACCESS"."WNL-UTILS"."STG__PYTHON_FILES" to role "ANALYST";

list '@"EXTERNAL_ACCESS"."WNL-UTILS"."STG__PYTHON_FILES"/wnl-utils/';
