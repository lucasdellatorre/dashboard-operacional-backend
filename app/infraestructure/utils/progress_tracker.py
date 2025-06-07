import redis
import json
from app.infraestructure.utils.logger import logger
from app.infraestructure.utils.enviroment import ENVIRONMENT


env = ENVIRONMENT().get_instance()

r = redis.Redis(
    host=env.getRedisHost(),
    port=int(env.getRedisPort()),
    decode_responses=True
)

def set_job_metadata(job_id: str, nome: str, size: int, data_upload: str):
    r.set(f"job:{job_id}:meta", json.dumps({
        "job_id": job_id,
        "nome": nome,
        "size": size,
        "data_upload": data_upload
    }))

def set_progress(job_id: str, status: str, progress: int, erro: bool = False, mensagem: str = None, ttl_seconds: int = 60):
    r.set(
        f"job:{job_id}",
        json.dumps({
            "status": status,
            "progress": progress,
            "erro": erro,
            "mensagem": mensagem
        }),
        ex=ttl_seconds
    )

def get_progress(job_id: str):
    raw = r.get(f"job:{job_id}")
    if raw:
        return json.loads(raw)
    return {
        "status": "not found",
        "progress": 0,
        "erro": True,
        "mensagem": "Job não encontrado"
    }

def get_all_pending_jobs():
    jobs = []
    cursor = 0

    while True:
        cursor, keys = r.scan(cursor=cursor, match="job:*", count=100)
        for key in keys:
            if key.endswith(":meta"):
                continue  # ignora metadata por enquanto
            job_id = key.split(":", 1)[1]
            progress_raw = r.get(key)
            if not progress_raw:
                continue

            progress_data = json.loads(progress_raw)

            # logger.info("erro: " + progress_data.get("erro"))
            
            if progress_data.get("erro") == True or progress_data.get("status") == "Concluído":
                continue

            # Busca metadados
            meta_raw = r.get(f"job:{job_id}:meta")
            if not meta_raw:
                continue  # ignora se não tiver metadados

            meta = json.loads(meta_raw)
            jobs.append(meta)

        if cursor == 0:
            break

    return jobs