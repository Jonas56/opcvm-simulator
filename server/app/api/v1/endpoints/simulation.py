"""
Simulation-related API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.services.simulation_service import SimulationService
from app.schemas.simulation import (
    SimulationInput, 
    MonteCarloInput, 
    SimulationResult, 
    MonteCarloResult
)

router = APIRouter()


@router.post("/deterministic", response_model=SimulationResult)
def deterministic_simulation(
    simulation_input: SimulationInput,
    db: Session = Depends(get_db_session)
):
    """
    Perform deterministic investment simulation.
    
    This endpoint calculates a deterministic projection of investment returns
    based on historical fund performance data.
    """
    try:
        result = SimulationService.deterministic_simulation(db, simulation_input)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")


@router.post("/monte-carlo", response_model=MonteCarloResult)
def monte_carlo_simulation(
    simulation_input: MonteCarloInput,
    db: Session = Depends(get_db_session)
):
    """
    Perform Monte Carlo investment simulation.
    
    This endpoint runs multiple simulations with random variations to provide
    statistical analysis of potential investment outcomes.
    """
    try:
        result = SimulationService.monte_carlo_simulation(db, simulation_input)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Monte Carlo simulation failed: {str(e)}")
