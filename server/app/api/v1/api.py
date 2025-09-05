"""
Main API router for v1 endpoints.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import funds, simulation, health

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(funds.router, prefix="/funds", tags=["funds"])
api_router.include_router(simulation.router, prefix="/simulation", tags=["simulation"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
