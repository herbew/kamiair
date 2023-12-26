# kamiair
Repository for KAMI Airlines

# Deploment Step
This service, running on Ubuntu 22.04
see. at deployment steps detail on /kamiair/guidances/ubuntu-deployment.rst

# Test
source envkamiair/bin/activate
cd kamiair/
python3 manage.py test -v 2 tests

# RUN
source envkamiair/bin/activate
cd kamiair/
python3 manage.py runserver 0.0.0.0:8000

# Test by the postman and the local browser
Url:
http://<ip>:8000/api/get/assumption/1/passenger/80/

Result:
--------------------------------------------------------------------------------
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/vnd.api+json
Vary: Accept

{
    "links": {
        "first": "http://192.168.1.8:8000/api/get/assumption/1/passenger/80/?page%5Bnumber%5D=1",
        "last": "http://192.168.1.8:8000/api/get/assumption/1/passenger/80/?page%5Bnumber%5D=1",
        "next": null,
        "prev": null
    },
    "data": [
        {
            "type": "PassengerAssumptions",
            "id": "9",
            "attributes": {
                "aircraft": {
                    "id": 1,
                    "airline": {
                        "id": 1,
                        "code": "KAMI",
                        "name": "KAMI Airlines"
                    },
                    "tail_number": "KM-001",
                    "fuel_capacity": 200.0,
                    "fuel_consume": 1.25,
                    "fuel_consume_add": 0.0025
                },
                "total_passenger": 80,
                "max_minutes": 137.93103448275863
            }
        }
    ],
    "meta": {
        "pagination": {
            "page": 1,
            "pages": 1,
            "count": 1
        }
    }
}
--------------------------------------------------------------------------------






