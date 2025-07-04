# Webhook Integration

This repository supports webhook-based updates from external add-on repositories. When you create a new release in your add-on repository, you can automatically trigger an update in this repository.

## How It Works

1. **Repository Dispatch Event**: External repositories can trigger a `repository_dispatch` event
2. **Automatic Update**: The workflow will clone your repository and update the add-on
3. **Version Sync**: The version in `.addons.yml` will be automatically updated

## Setting Up Webhooks

### 1. Create a Personal Access Token

1. Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Give it a name like "Add-on Repository Webhook"
4. Select the `repo` scope
5. Copy the generated token

### 2. Configure Your Repository

Add this workflow to your add-on repository (`.github/workflows/notify-updates.yml`):

```yaml
name: Notify Add-on Repository

on:
  release:
    types: [published]

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Notify add-on repository
        run: |
          curl -X POST \
            -H "Accept: application/vnd.github.v3+json" \
            -H "Authorization: token ${{ secrets.ADDON_REPO_TOKEN }}" \
            https://api.github.com/repos/m2sh/ha-addons/dispatches \
            -d '{
              "event_type": "addon-update",
              "client_payload": {
                "addon": "your-addon-name",
                "version": "${{ github.event.release.tag_name }}"
              }
            }'
```

### 3. Add Repository Secret

In your add-on repository:
1. Go to Settings > Secrets and variables > Actions
2. Create a new secret named `ADDON_REPO_TOKEN`
3. Paste the personal access token from step 1

## Manual Updates

You can also trigger updates manually:

### Via GitHub Actions UI
1. Go to the Actions tab in this repository
2. Select the "CI" workflow
3. Click "Run workflow"
4. Optionally specify an add-on name
5. Click "Run workflow"

### Via API
```bash
curl -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/repos/m2sh/ha-addons/dispatches \
  -d '{
    "event_type": "addon-update",
    "client_payload": {
      "addon": "chisel"
    }
  }'
```

## Scheduled Updates

The repository also runs daily updates at 2 AM UTC to check for new versions of all add-ons.

## Supported Events

- `addon-update`: Triggers an update for a specific add-on
- `workflow_dispatch`: Manual trigger with optional add-on parameter
- `schedule`: Daily automatic updates

## Example: Chisel Add-on

For the chisel add-on, the webhook payload would be:

```json
{
  "event_type": "addon-update",
  "client_payload": {
    "addon": "chisel",
    "version": "1.10.1"
  }
}
```

## Troubleshooting

### Common Issues

1. **Permission Denied**: Make sure your token has the `repo` scope
2. **Add-on Not Found**: Verify the add-on name matches exactly in `.addons.yml`
3. **Branch Issues**: Ensure the source repository has the expected branch

### Debugging

Check the workflow logs in the Actions tab to see detailed output from the update process.

## Security

- Only use personal access tokens with minimal required permissions
- Consider using GitHub Apps for more granular control
- Regularly rotate your tokens
- Monitor webhook usage in your repository settings 