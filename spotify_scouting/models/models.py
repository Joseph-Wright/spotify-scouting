from pydantic import BaseModel

class Sliders(BaseModel):
    targetAcousticness: int
    targetLiveness: int
    targetDanceability: int
    targetValence: int
    targetEnergy: int
    targetPopularity: int

class SubmitRequest(BaseModel):
    userInput: str
    byArtist: bool
    sliderValues: Sliders
