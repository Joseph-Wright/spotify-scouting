from pydantic import BaseModel


class SubmitRequest(BaseModel):
    userInput: str
    byArtist: bool
    randomize: bool
    slider1: int
    slider2: int
    slider3: int
    slider4: int
    slider5: int
    slider6: int