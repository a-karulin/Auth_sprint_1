from sqlalchemy.orm import Session


def get_session():
    def wrapper(func):
        def inner(self, *args, **kwargs):
            with Session(self.engine) as session:
                return func(self, *args, **kwargs, session=session)

        return inner

    return wrapper
