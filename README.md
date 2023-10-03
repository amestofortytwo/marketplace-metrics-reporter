# Azure AD Group User Reporter 📊

This application fetches the number of users in an Azure AD group and reports the number to Azure Marketplace Metering Service.

## Environment Variables 🛠️

To run the container, you'll need to provide the following environment variables:

- **TENANT_ID** 🆔
  - Represents the Tenant ID of your Azure AD.

- **CLIENT_ID** 🔑
  - The Microsoft Entra Identity Application ID.

- **CLIENT_SECRET** 🤫
  - Secret associated with the Microsoft Entra Identity Application.

- **RESOURCE** 🌐
  - URL endpoint of the Azure service you're accessing, typically `https://cloudapi.deployment.marketplace.azure.com/`.

- **METER_ID** 📏
  - ID that you've set for your metering dimension in Azure Marketplace.

- **CUSTOMER_SUBSCRIPTION_GUID** 📄
  - Provided when a customer subscribes to your application in Azure Marketplace.

- **RESOURCE_GUID** 🏷️
  - Your marketplace resource ID.

Please ensure these environment variables are set correctly for the application to function properly.
