# Climate-Adjusted Property Valuation Project Status

## 1. Project Overview

This project is a climate-adjusted property valuation backend designed to estimate a property's market value after accounting for climate-related risk factors. The system uses historical and spatial risk indicators such as flood exposure, heat stress, and cyclone impact to adjust the base valuation.

The solution is currently structured as a FastAPI-based backend prototype and is intended to serve as a base for a broader property-risk analytics product.

---

## 2. Current Status

### Completed
- Reorganized the app into a cleaner backend structure
- Converted the project from a loose prototype into a FastAPI application
- Added proper app-level config and schema validation
- Documented the project usage in the main README
- Added smoke tests for API endpoints
- Verified the API health and prediction endpoints
- Pushed the repository to GitHub

### In Progress / Prototype-Level
- Research-grade climate data processing
- Model validation and business rule calibration
- Production deployment setup
- Database integration
- Authentication and user management
- Monitoring, logging, and alerting

### Not yet Production-Ready
- Secure environment management
- Production-grade error handling
- API rate limiting
- Multi-user data access
- Persistent storage of valuation requests
- CI/CD configuration
- Dockerization / deployment packaging

---

## 3. Functional Scope

The current system supports the following:

1. Base property valuation based on area and market rate per sqft
2. Flood exposure lookup using raster data
3. Heat risk lookup using district/block data
4. Cyclone exposure using historical storm tracks
5. Climate risk aggregation using weighted scoring
6. Final adjusted valuation output
7. JSON API endpoint for prediction requests

---

## 4. Main Application Files

- `main.py` - repository root compatibility wrapper
- `TamilNadu-Climate-Property/app/main.py` - FastAPI application entry
- `TamilNadu-Climate-Property/app/climate_engine.py` - core valuation logic
- `TamilNadu-Climate-Property/app/config.py` - configuration and dataset paths
- `TamilNadu-Climate-Property/app/schemas.py` - request validation models
- `TamilNadu-Climate-Property/tests/test_api.py` - app smoke tests

---

## 5. Application Workflow

The workflow is:

1. Receive property details from API request
2. Extract district, city, coordinates, area, and market rate
3. Evaluate flood exposure from the flood raster
4. Evaluate heat risk from district/block risk data
5. Evaluate cyclone risk from nearby historical storm tracks
6. Aggregate the climate factors into a weighted risk score
7. Compute a discount percentage
8. Return the adjusted property value and risk breakdown

---

## 6. API Endpoint

### Health Check
- `GET /`

Returns app status and metadata.

### Prediction
- `POST /predict`

Request fields:
- district
- city
- latitude
- longitude
- area_sqft
- market_rate_per_sqft

Output includes:
- base value
- risk score
- adjustment percentage
- adjusted value
- flood exposure
- heat risk details
- cyclone details
- data completeness

---

## 7. Data Sources Used

### Flood Data
- Raster datasets inside `data/flood/`
- Used for spatial flood hazard estimation

### Heat Data
- CSV and JSON datasets inside `data/heat/`
- Used for district/block heat risk inference

### Cyclone Data
- Historical storm track files inside `data/cyclone/`
- Used for nearby cyclone and wind exposure estimation

### Property Data
- Property and valuation datasets under `data/property/`
- Used for valuation and research experimentation

---

## 8. Key Limitations

This is not yet a final business-grade valuation system because:

- climate weights are manually defined and not calibrated with live market data
- flood lookup depends on GDAL tool availability
- risk model is rule-based and may not be statistically validated
- data completeness may vary depending on the district/location
- there is no persistent system of storing or auditing predictions
- deployment environment is not hardened

---

## 9. Verification Status

The backend has been verified using tests:

- Health route passes
- Prediction route passes

This confirms the API is functional in its current prototype state.

---

## 10. Recommended Next Milestones

### Short-Term Goals
- Improve API architecture (routers + services)
- Add environment-variable config
- Add stronger validation and standard output models
- Add database storage for predictions
- Improve README and setup instructions

### Medium-Term Goals
- Create a deployable Docker setup
- Add CI/CD pipeline
- Add monitoring and logging
- Improve dataset processing and validation
- Expand risk modeling with market calibration

### Long-Term Goals
- Production-grade property valuation platform
- Frontend dashboard integration
- ML model improvement with validated historical sales data
- Multi-state / national coverage
- Enterprise-grade security and compliance

---

## 11. Final Assessment

The project is in a solid prototype-to-backend phase. The foundation is working, the API is usable, and the repo is organized well enough to continue development. However, it is still a research and backend prototype rather than a complete commercial application.

The current state should be viewed as a successful proof of concept and technical foundation for future productization.
