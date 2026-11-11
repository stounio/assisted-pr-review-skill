# Review questions by area

Ask the questions of each area the change touches. A change often touches several areas: a new endpoint usually involves the API, endpoint, data types and tests areas.

A nested question is a follow-up: answer it when its parent question's answer is Yes or Partly.

## API (any API)

- Are the changes to the API contract backward compatible?
- Is the API contract verified with a Pact test between a consumer and a provider?
- Is the documentation in the API specification up to date?
- Are the types aligned with the ones already in use in the API?

## Public API

- Is there a changelog entry describing the change introduced to the Public API?
- Has the version of the Public API been updated?
- Does the API pass the smoke tests?

## Implementation

- What is the risk of deploying this change to production?
- Should the change be gated behind a feature flag?
- How should this change be monitored?
- Is there a test that verifies the targeted outcome?
- Does the implementation introduce a new pattern for a type of work the codebase already does?
- Are inline comments needed?
  - Should the commented behaviour be covered by a test instead, so the comment can be removed?
- Does a function have multiple exit points?
- Does a function name, boolean or condition use a negation?
  - Can it be phrased affirmatively?
- Does a function contain a guard clause?
  - Should the check move closer to where the data enters the system?
- Are failures handled, logged and surfaced to the caller consistently with the rest of the codebase?

## Endpoint

### New endpoint

- Is there an existing endpoint suitable to support the requirement?
- Is there an existing endpoint that can be extended to support the requirement?
- Is the data access pattern of the new endpoint aligned with existing access patterns?
- Is the data access pattern secure?
- Does the endpoint apply a security policy in accordance with its intended usage?

### Updated endpoint

- Is the endpoint secured according to its intended usage?
- Is a migration plan required to move existing consumers onto the endpoint's new security policy?

## Data types

- Are types and attributes named according to the domain language?
- Should each attribute be nullable or mandatory?
- Do nullable attributes have a default value?
- Are tiny types used for attributes?
- Should an attribute's supported values be an enumeration?
- Is there an existing type suitable to model the data?

## Database migrations

- Is the migration backward compatible with the version of the application currently running?
- Is the migration safe to run under live traffic?
- Can the migration be rolled back?
- Is the migration covered by a test against the target database engine?

## Events and messages

- Is the change to the message schema backward compatible with existing consumers?
- Can consumers still read messages already published with the previous schema?
- Is the schema change registered or documented where consumers discover it?
- Is the message handling idempotent?

## Dependencies

- Is the new dependency needed, or does an existing dependency already cover the need?
- Is the dependency maintained, and is its licence compatible with the project?
- Does the version bump introduce breaking changes?

## Tests

- Does each test improve the coverage of the implementation?
- Was the test written to fail first?
- Does a test cover a use case that no longer exists in the implementation?

## Frontend

- Does the change embed business logic not directly related to the frontend?
  - Should that logic move to a backend layer that encapsulates the business function?
- Is the change to a UI component accessible?
- Does the frontend call a backend API through an existing client and handle its errors?
