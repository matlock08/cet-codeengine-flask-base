# IBM Code Engine template

## Requirements
- Instance of Watson Discovery Plus/Enterprise plan on IBM Cloud.

## Setup Instructions

### Deploy the webhook enrichment app to Code Engine


1. Deploy the application from this repository source code.
   - In **Create application**, click **Specify build details** and enter the following:
      - Source
         - Code repo URL: `https://github.com/matlock08/cet-codeengine-flask-base
         - Code repo access: `None`
         - Branch name: `master`
         - Context directory: ``
      - Strategy
         - Strategy: `Dockerfile`
      - Output
         - Enter your container image registry information.

   
   - We recommend setting **Min number of instances** to `1`.

4. Confirm that the application status changes to **Ready**.

