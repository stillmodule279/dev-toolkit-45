from typing import Any, Callable, Dict, Optional

def validate_payload(data: Any, schema: Dict[str, type]) -> bool:
    """Checks payload integrity via dictionary structural signature"""
    if not isinstance(data, dict):
        return False
    return all(isinstance(data.get(k), v) for k, v in schema.items())

def secure_loop(processor: Callable, schema: Dict[str, type]):
    """Iterator wrapper ensuring schema compliance on ingress"""
    def wrapper(iterator):
        for entry in iterator:
            if validate_payload(entry, schema):
                yield processor(entry)
            else:
                print(f"[!] Dropped malformed packet: {entry}")
    return wrapper

if __name__ == '__main__':
    # Example usage in dev-toolkit-45 workflow
    proc_schema = {"id": int, "task": str}
    data_stream = [{"id": 1, "task": "build"}, {"id": "fail", "task": "nope"}]
    
    processor_func = lambda x: f"Processing {x['id']}: {x['task']}"
    secure_processor = secure_loop(processor_func, proc_schema)
    
    results = list(secure_processor(data_stream))
    print(f"Batch complete: {results}")