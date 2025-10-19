# # app/db/base.py

# from abc import ABC, abstractmethod

# # This is not used currently.
# # TODO: make a mongo adapter class that implements this interface
# class DatabaseAdapter(ABC):
#     """Abstract DB interface."""

#     @abstractmethod
#     async def connect(self):
#         """Connect to the database."""
#         pass

#     @abstractmethod
#     async def create_indexes(self):
#         """Create necessary indexes or constraints."""
#         pass

#     @abstractmethod
#     async def close(self):
#         """Close the connection."""
#         pass
