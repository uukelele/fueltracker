from pydantic import BaseModel
from typing import Optional

class APIResponseData(BaseModel):
    redirectUrl: str
    fileName: str
    generated_at: str

class APIResponse(BaseModel):
    """
    {
        "success": true,
        "data": {
            "redirectUrl": "https://ff-raw-data-bronze-ics-prod.s3.eu-west-2.amazonaws.com/UpdatedFuelPrice-1775746800057.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAUJYP2NSFM4TPQ5NR%2F20260409%2Feu-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260409T172729Z&X-Amz-Expires=43200&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEFIaCWV1LXdlc3QtMiJGMEQCIExgyVG7NYbpIERZrAbNgwSYbsKprMbmuc2S3z4dHNPPAiBheygU77j52fY7xZvu8qf9zCzPhNHPjTpe4dM4BpVXNSqRBQgbEAAaDDI5NTg0OTA2MTUxNCIMJvdMRKEcnafKiUV3Ku4EUEsxLzO1i7s782%2BB%2BkenCMKn5qHlQ6i%2B8gYAs1Xh29BwwlWXGM4WLQn8Wl006tYDavLCcCjoEWXtx6f23iQXWO0v68Ji7Ig5%2FRXl7VXaZ7qHu0EkGXF2yQOXBGfI4KhUUHCl108GawWrKW4rBiYgAFRJk0tMbIHaaeZeCI6xFlXDKuSx%2BkMgACoCvIbH6Mi8FJZYzTrRvbjxwWVG2erHaKLi09xQLC8QqoRBF5QIWPqHpohb9L2o4jWLLYtx7nlWsXQtZBlm5fzDSXJqbJqv6%2BY3Lf4tewckM9ZfySIZDN0uX8sw8zRh8ZVg2iazuDFmplcRJRWMtA2unSTr32uuDOxJYbT4qQE2ODlC8dExcmh6uZNGI84uQYoaTd8%2Fpl6awCifgZ12%2FRMYinSk2gRtHPAcNoQ01d9tO7G1Jl9kUzES5jzCkqqTsSmiJghG5O9yOfyi3F1zjopfUXT54WQ1v8OsM8XNl%2BY629eP%2BS0cFpNXo%2BexFrjT6H4WC0lqlwaWu8t5MxEeoGjxAWqiqeOuYwGcbwKOnbv8mFRdSZBnmNb9BPZAmhxuY6Y39p9X4Sn2gwnMDtLwelobe4fWrtUEuw4meRSkGV3j0gXYgJN1oU3zNErMGEdwwKwtzeV50zdfWCCsFwmKArXIApvLq7Mi%2BC7FYZc78vnNdd4egL33dX29BkdxQP%2BRotq8%2Fbuk6NUZIB%2B3ka6tQx7wnsruqevqLETOwDhT5mEQw36Lr5QoBu95NNTIHvsZM1FFMTYERx7Nym3sYwl21OvTyf%2F883TPifsLyD74h8dvKxJxWWD1UI%2F1QaGNorD9BrfzRw30YDCBw9%2FOBjqaAZxeYZyGZM0MptmgbsWQGkkHjfN8AZxWa%2B1yUiXf0CHJIvI3YoyyhF11i0IKSgY5MTY6Q34jmqzs47iNZmQL%2BIiGWG6oNOvOrBNL2uxy91dJ3X3ovE8FjiFsH5Z6aVJxU3ie49wWIh89eHnilXLhGM3PAOfruaLnRd0b1TYech0bvXFcC7U9eEvwgGRYqgsE01seGtn6fC4lEIs%3D&X-Amz-Signature=4fca6cd2f9d63736f5b1b2ab57e89f385e5f000760aeadbe6fde6853766eaecd&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject",
            "fileName": "UpdatedFuelPrice-1775746800057.csv",
            "generated_at": "2026-04-09T15:00:37.291Z"
        },
        "message": "Operation successful"
    }
    """
    success: bool
    data: APIResponseData
    message: str


class Location(BaseModel):
    postcode: Optional[str]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    city: Optional[str]
    county: Optional[str]
    country: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]


class FuelPrice(BaseModel):
    E5: Optional[float]
    E10: Optional[float]
    B7S: Optional[float]
    B7P: Optional[float]
    B10: Optional[float]
    HVO: Optional[float]


class PriceTimestamp(BaseModel):
    E5: Optional[str]
    E10: Optional[str]
    B7S: Optional[str]
    B7P: Optional[str]
    B10: Optional[str]
    HVO: Optional[str]


class DayOpening(BaseModel):
    open_time: Optional[str]
    close_time: Optional[str]
    is_24_hours: Optional[bool]


class UsualDays(BaseModel):
    monday: DayOpening
    tuesday: DayOpening
    wednesday: DayOpening
    thursday: DayOpening
    friday: DayOpening
    saturday: DayOpening
    sunday: DayOpening


class BankHolidayStandard(BaseModel):
    open_time: Optional[str]
    close_time: Optional[str]
    is_24_hours: Optional[bool]


class BankHoliday(BaseModel):
    standard: BankHolidayStandard


class OpeningTimes(BaseModel):
    usual_days: UsualDays
    bank_holiday: BankHoliday


class FuelEnergyServices(BaseModel):
    adblue_pumps: Optional[bool]
    adblue_packaged: Optional[bool]
    lpg_pumps: Optional[bool]


class VehicleServices(BaseModel):
    car_wash: Optional[bool]


class Amenities(BaseModel):
    fuel_and_energy_services: FuelEnergyServices
    vehicle_services: VehicleServices
    air_pump_or_screenwash: Optional[bool]
    water_filling: Optional[bool]
    twenty_four_hour_fuel: Optional[bool]
    customer_toilets: Optional[bool]


class Forecourts(BaseModel):
    node_id: str
    trading_name: Optional[str]
    brand_name: Optional[str]
    is_motorway_service_station: Optional[bool]
    is_supermarket_service_station: Optional[bool]
    public_phone_number: Optional[str]
    temporary_closure: Optional[bool]
    permanent_closure: Optional[bool]
    permanent_closure_date: Optional[str]

    location: Location
    fuel_price: FuelPrice
    price_submission_timestamp: PriceTimestamp
    price_change_effective_timestamp: PriceTimestamp
    opening_times: OpeningTimes
    amenities: Amenities


class ForecourtRecord(BaseModel):
    forecourt_update_timestamp: Optional[str]
    forecourts: Forecourts