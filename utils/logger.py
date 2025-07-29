from functools import wraps

def simple_logger(func):

        private_keywords = {"api_key", "bearer", "authorization", "headers", "analytics", "client_id", "client_secret", "grant_type", "token_type", "expires_in", "access_token", "token", "pma_username", "pma_password"}

        def mask_private_data(data):
            if isinstance(data, dict):
                return {
                    str(k): (mask_private_data(v) if not any(kw in str(k).lower() for kw in private_keywords) else "***hidden***")
                    for k, v in data.items()
                }
            elif isinstance(data, list):
                return [mask_private_data(item) for item in data]
            elif isinstance(data, tuple):
                return tuple(mask_private_data(item) for item in data)
            elif isinstance(data, str):
                return "***hidden***" if any(kw in data.lower() for kw in private_keywords) else data
            else:
                return data
            
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.logger:
                masked_args = mask_private_data(args)
                masked_kwargs = mask_private_data(kwargs)
                self.logger.debug(f'Запуск метода {func.__name__}() с args={masked_args}, kwargs={masked_kwargs}')
            try:
                result = func(self, *args, **kwargs)
                return result
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Ошибка в {func.__name__}(): {e}")
                raise

        return wrapper
