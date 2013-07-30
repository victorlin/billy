from __future__ import unicode_literals

from flask import request
from flask.ext.restful import marshal_with

from api.errors import BillyExc
from api.resources.group import GroupController
from models import Group, Customer, PayoutInvoice, PayoutSubscription
from view import payout_inv_view


class PayoutInvIndexController(GroupController):
    """
    Base PayoutInvoice resource used to create a payout invoice or
    retrieve all your payout invoices
    """

    @marshal_with(payout_inv_view)
    def get(self):
        """
        Return a list of payout invoices pertaining to a group
        """
        return PayoutInvoice.query.join(PayoutSubscription).join(Customer).join(
            Group).filter(Group.guid == self.group.guid).all()


class PayoutInvController(GroupController):
    """
    Methods pertaining to a single payout invoice
    """

    def __init__(self):
        super(PayoutInvController, self).__init__()
        payout_inv_id = request.view_args.values()[0]
        self.invoice = PayoutInvoice.query.filter(
            PayoutInvoice.guid == payout_inv_id).first()
        if not self.invoice:
            raise BillyExc['404_PAYOUT_INV_NOT_FOUND']

    @marshal_with(payout_inv_view)
    def get(self, payout_inv_id):
        """
        Retrieve a single invoice
        """
        return self.invoice