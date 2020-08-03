import operator
from datetime import timedelta
import tldextract
from dateutil.parser import parse
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator

ORDER = []
EMAIL = []
app = FastAPI()


class Order(BaseModel):
    order_id: int
    cust_id: str
    product_name: str
    domain: str
    duration_months: int
    start_date: str


#This class is for Domain Orders
class DomainOrder(Order):

    #These are validator's for my data that were being entered.
    #.org or .com for top lvl domain
    @validator('domain')
    def domain_must_be_com_org_edu(cls, v):
        domainext = tldextract.extract(v)
        if domainext.suffix != 'com' and domainext.suffix != 'org':
            raise ValueError('must be a .com or .org domain')
        return v

    # unique top level domains only.
    @validator('domain')
    def domain_must_be_unique(cls, v):
        #get domain entries from the db and validate for uniqueness
        global ORDER
        result = [Domain_Order for Domain_Order in ORDER if Domain_Order.domain == v]
        if result:
            raise ValueError('Must be a unique domain')
        return v

    #must be increments of a year (12 months) duration
    @validator('duration_months')
    def duration_months_must_be_positive(cls,v):
        if v % 12 != 0:
            raise ValueError('Must be an int greater than 0 months and be in 12 month increments(1 year)')
        return v

#Allows you to see all orders placed and they are sorted.
@app.get("/orders/")
def list_orders():
    global ORDER
    ORDER.sort(key=operator.attrgetter('cust_id'))
    return ORDER


#Allows you to see all emails that are scheduled and they are sorted.
@app.get("/Email/")
def list_emails():
    global EMAIL
    EMAIL.sort(key=lambda x: x.get('email_date'), reverse=False)
    return EMAIL


#This allows you to enter an order
@app.put("/orders")
def add_order(order: DomainOrder):
    global ORDER
    if billing(order, True):
        if register_domain(order, True):
            try:
                ORDER.append(order)
                dom_date = parse(order.start_date)
                dom_date2 = dom_date + timedelta(days=363)
                schedule_email(order.cust_id, order.product_name, order.domain, dom_date2.strftime("%m/%d/%Y"))
                return {"order_id": order.order_id, "cust_id": order.cust_id, "product_name": order.product_name, "domain": order.domain, }
            except TypeError as e:
                register_domain(order, False)
                #This is to roll-back what completed before the error.
                billing(order, False)
                raise HTTPException(status_code=404, detail='Unable to add order')
        else:
            # This is to roll-back what completed before the error.
            billing(order, False)
            raise HTTPException(status_code=404, detail='Registration failed')
    else:
        raise HTTPException(status_code=404, detail='Billing Failed')


def billing(order, a):
    #this is where I would put the code for billing or I could call some other service that handled billing
    return True


def register_domain(order, a):
    #This is where I would put the code for registering a domain or I would call another service that handles that.
    return True

#This schedules the emails.
def schedule_email(cust_id, product_name, domain, date):
    global EMAIL
    EMAIL.append({'cust_id': cust_id, 'product_name': product_name, 'domain': domain, 'email_date': date})
    return True


