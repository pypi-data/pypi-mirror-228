import httpx
from prefect import task, get_run_logger, flow
from prefect.server.api.ui.flow_runs import SimpleFlowRun

from prefect_supporter.model.clearing_db import FlowRunClearing


@task
async def clear_flow_run_task(frc: FlowRunClearing):
    logger = get_run_logger()
    client = httpx.AsyncClient(base_url=frc.api_url)
    offset: int = 0
    _limit = 1000

    while True:
        logger.info(f"offset: {offset} limit: {_limit}")
        res = await client.post(url=f"/ui/flow_runs/history", json={
            "limit": _limit,
            "offset": offset,
            "sort": "START_TIME_DESC",
            "flow_runs": {
                "state": {
                    "operator": "and_",
                    "type":
                        {
                            "any_": frc.state_list
                        }
                },
                "expected_start_time":
                    {
                        "before_": frc.before_dt.strftime("%Y-%m-%d %H:%M:%S.%f"),
                        "after_": frc.after_dt.strftime("%Y-%m-%d %H:%M:%S.%f"),
                    }
            }
        })
        logger.info(res.text)
        res.raise_for_status()
        flow_run_list: list[SimpleFlowRun] = [SimpleFlowRun.parse_obj(r) for r in res.json()]

        for fr in flow_run_list:
            res2 = await client.delete(url=f"/flow_runs/{fr.id}")
            logger.info(res2.text)
            res.raise_for_status()
        if len(flow_run_list) < _limit:
            break
        else:
            offset += 1


@flow
def clear_db_history_flow(frc: FlowRunClearing):
    clear_flow_run_task(frc)
