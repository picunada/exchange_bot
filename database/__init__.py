from .connect import metadata, engine

metadata.create_all(bind=engine)
