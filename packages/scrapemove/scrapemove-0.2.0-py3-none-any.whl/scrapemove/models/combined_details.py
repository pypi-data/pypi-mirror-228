from pydantic import BaseModel, HttpUrl

from scrapemove.models.property_details_screen import PropertyDetails
from scrapemove.models.results_screen import Property


class CombinedDetails(BaseModel):
    property: Property
    additional_details: PropertyDetails

    def dump(self):
        return self.dict()
    
    @classmethod
    def load(cls, data):
        return cls.parse_obj(data)
