1️⃣ Create docs/api.md

Inside your docs folder, create api.md.

Put this as a starting version and then tweak names if your URLs differ:

# Subscriptly API Documentation

## Overview

Subscriptly is a multi-tenant subscription platform.  
Core concepts:
- **Tenant** – an organization/workspace.
- **Plan** – a billing plan (Basic, Pro…).
- **Subscription** – which plan a tenant is on.
- **Invoice** – a billing record for a tenant and plan.

Authentication is required for most endpoints.

---

## Authentication

Most endpoints expect a logged-in user with a valid token.

Send the token in the `Authorization` header:

```http
Authorization: Bearer <your_jwt_token>
 this if you’re using a different auth mechanism.)

Tenants

Base path (from your urls):
/api/tenants/

1. Create Tenant

Endpoint

POST /api/tenants/create/


Auth: Required (user must be authenticated)

Request body (JSON)

{
  "name": "My First Org"
}


Behavior

Creates a new Tenant with the given name.

Sets the owner of the tenant to the authenticated user.

Automatically assigns a trial subscription (via assign_trial_subscription).

Creates an owner membership for the user on that tenant.

Responses

201 Created – tenant created successfully

Body: serialized tenant (at least id, name, owner).

400 Bad Request – invalid data

Example: missing name, duplicate tenant name.

401 Unauthorized – if request has no valid authentication.

2. Get Current User Tenant Info

Endpoint

GET /api/tenants/me/


Auth: Required

Description

Returns information about the tenant(s) associated with the current user, or the “active” tenant, depending on your implementation.

Responses

200 OK – tenant data for the authenticated user.

401 Unauthorized – if no valid token is provided.

3. Tenant Admin Check (Example)

Endpoint

GET /api/tenants/admin/check/


Auth: Required

Description

An example admin-only endpoint to verify if the user has admin/owner permissions for the current tenant.

Responses

200 OK – user has admin/owner access.

403 Forbidden – user is authenticated but does not have admin rights.

401 Unauthorized – not authenticated.

Plans

Base path (from your project):
/api/plans/

1. List Plans

Endpoint

GET /api/plans/


Auth: (Decide as per your design)

Often: public (no auth) OR

Auth required (for app-only usage)

Description

Returns the list of active billing plans that tenants can subscribe to.

Plan fields (from model)

name (string, unique)

price (decimal)

duration_days (integer, e.g. 30)

quota (integer – allowed resources)

description (string, optional)

is_active (boolean)

Sample Response

[
  {
    "id": 1,
    "name": "Basic",
    "price": "10.00",
    "duration_days": 30,
    "quota": 100,
    "description": "",
    "is_active": true
  },
  {
    "id": 2,
    "name": "Pro",
    "price": "20.00",
    "duration_days": 30,
    "quota": 200,
    "description": "",
    "is_active": true
  }
]


Responses

200 OK – list of active plans.

Subscriptions

Currently, subscription state is mostly internal, not exposed via public API (based on our work so far).
This section documents the behavior, not an endpoint.

Model

tenant – OneToOne to Tenant

plan – FK to Plan

start_date – subscription start

end_date – optional end

is_active – whether subscription is active

is_trial – whether subscription is a trial

created_at – creation timestamp

Default behavior

When a tenant is created:

A Subscription is created for that tenant.

Typically: is_active = True, is_trial = True for trial subscriptions (depending on your assign_trial_subscription logic).

You can later add endpoints like:

GET /api/subscriptions/me/ – current tenant subscription

POST /api/subscriptions/change-plan/ – change plan

(You don’t need them now for Day 14, but you can document them when implemented.)

Invoices

Invoices are generated internally using InvoiceService.

Model (Invoice)

tenant – FK to Tenant

plan – FK to Plan

subscription – FK to billing.Subscription

amount – decimal

status – one of: pending, paid, failed

created_at

due_date

paid_at

Key methods

mark_paid() – sets:

status = "paid"

paid_at = now()

mark_failed() – sets:

status = "failed"

InvoiceService

InvoiceService.generate_invoice(subscription)


Creates an invoice for the given subscription with:

tenant = subscription.tenant

plan = subscription.plan

amount = subscription.plan.price

status = pending

due_date = now

This method is intended to be used in your billing flows (e.g. on successful subscription, renewal, etc).

Right now, this is internal behavior, not exposed as a public API endpoint yet.

Error Handling

Common response codes:

200 OK – successful GET

201 Created – new resource created

400 Bad Request – validation error (missing fields, duplicates, invalid data)

401 Unauthorized – missing/invalid authentication

403 Forbidden – authenticated but lacking permissions

404 Not Found – endpoint or resource not found

Testing Notes (Day 14 Coverage)

Automated tests cover:

Tenant creation

creates tenant with correct owner

rejects missing name

rejects unauthenticated requests

rejects duplicate tenant name

Plan list

returns all active plans

Subscription

default state on creation (is_active, is_trial)

This ensures your API behavior matches the docs above.


You can tweak small details (like auth method wording) depending on your setup, but this is already solid and matches what you’ve built.

---

## 2️⃣ Mark Day 14 as complete

Once `docs/api.md` is created and saved:

```bash
git add .
git commit -m "tests for tenancy and plans"