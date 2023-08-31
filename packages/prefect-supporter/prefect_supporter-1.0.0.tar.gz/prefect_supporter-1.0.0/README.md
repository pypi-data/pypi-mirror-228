# prefect_supporter

prefect_supporter provide services to supporter to manage Prefect

## Usage

1. Delete `flow run` history in Database. It also deletes `task run`
   - create your deployment
      - example  
      ```python
      Deployment.build_from_flow(
        flow=clear_db_history_flow,
        name="clear_db_history_deployment",
        schedule=None,
        work_queue_name="default",
        tags=["prefect-management"],
        parameters={
            "frc": FlowRunClearing(
                state_list=[StateType.COMPLETED],
                before_dt=datetime.now(),
                after_dt=datetime(year=1970, month=1, day=1, hour=0, minute=0)
            )
        },
        apply=True
       )
      ```
  - Parameter   
      - `FlowRunClearing` model
         - api_url : your prefect api address, ex) http://localhost:4200/api
         - state_list: state list to delete ex) "COMPLETED", "FAILED"
         - before_dt : time range to delete data to be started
         - after_dt : time range to delete data  to be ended