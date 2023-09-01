import requests as rq
import xml.etree.ElementTree as ET
import re

class InvalidVATNumberError(Exception):
    """
    Exception thrown if there is a problem with regex validation
    """
    pass

class XMLParserError(Exception):
    """
    Exception thrown when there is a problem associated with xml parser
    """
    pass

class HTTPError(Exception):
    """
    Exception thrown when there is a problem associated with http response
    """
    pass

class VatRequest:
    _API_ENDPOINT = 'http://ec.europa.eu/taxation_customs/vies/services/checkVatTestService.wsdl'
    NAMESPACES = {"ns2": "urn:ec.europa.eu:taxud:vies:services:checkVat:types"}
    VAT_PATTERN = re.compile(r'^[0-9A-Za-z\+\*\.]{2,12}$')
    COUNTRY_PATTERN = re.compile(r'^[A-Z]{2}$')
    
    def __init__(self, country_code, vat_number):
        self.country_code = country_code 
        self.vat_number = vat_number
        
    def validate_api_request_parameters(self):
        is_country_valid = bool(self.COUNTRY_PATTERN.match(self.country_code))
        is_vat_valid = bool(self.VAT_PATTERN.match(self.vat_number))
        
        if not is_country_valid or not is_vat_valid:
            raise InvalidVATNumberError("Invalid country code or VAT number!")
    
    def send_soap_request(self):
        self.validate_api_request_parameters()

        body = f"""
                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:ec.europa.eu:taxud:vies:services:checkVat:types">
                <soapenv:Header/>
                <soapenv:Body>
                    <urn:checkVat>
                        <urn:countryCode>{self.country_code}</urn:countryCode>
                        <urn:vatNumber>{self.vat_number}</urn:vatNumber>
                    </urn:checkVat>
                </soapenv:Body>
                </soapenv:Envelope>
                """
        
        try:
            with rq.post(url=self._API_ENDPOINT, data=body) as response:
                response.raise_for_status()
                root = ET.fromstring(response.text)

                response_dict = {}

                for child in root.find(".//ns2:checkVatResponse", namespaces=self.NAMESPACES):
                    tag = child.tag.split("}")[1]  
                    text = child.text.strip() if child.text else ""
                    response_dict[tag] = text

            return response_dict
        
        except (rq.RequestException) as request_exception:
            raise HTTPError(f'HTTP error {request_exception}')
        except (ET.ParseError) as parsing_exception:
            raise XMLParserError(f'XML error {parsing_exception}')
    