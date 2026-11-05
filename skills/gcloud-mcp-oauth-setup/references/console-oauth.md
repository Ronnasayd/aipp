# Console steps: consent screen, scopes, test user, client

Observed with a browser automation tool against the Google Cloud console in pt-BR, for a personal account (External audience, testing mode). English names follow the vendor guide. Replace `PROJECT_ID` in every URL.

Sign-in is always done by the user. Verify each step by reading the page back, not by assuming the click worked.

## Technique

- Locate elements with a text or regex search of the accessibility snapshot instead of capturing the whole snapshot.
- After every save, reload the page and read the table. An empty table such as "Nenhuma linha a ser exibida" means nothing was saved.
- If a button seems inert, filter the network log for the console's OAuth backend calls (`OauthEntityService`). No new request after the click means the handler did not fire.

## 1. Branding (4-step wizard)

URL: `https://console.cloud.google.com/auth/overview/create?project=PROJECT_ID`

1. App name and user support email (a dropdown that lists the signed-in account).
2. Audience: External for a personal account. Internal is disabled outside an organization.
3. Contact email for change notices.
4. Accept the Google API Services User Data Policy, click Continue, then Create.

## 2. Test users

URL: `.../auth/audience?project=PROJECT_ID`, button "Add users".

- Type the address followed by a comma so it becomes a chip. The counter should read `1 / 100`.
- Clicking Save did not send a request in this automation. Pressing **Enter** while the Save button was focused worked.
- Confirm the address in the "Test users" table after reloading.

## 3. Scopes

URL: `.../auth/scopes?project=PROJECT_ID`, button "Add or remove scopes".

1. In "Manually add scopes", paste the scopes separated by commas.
2. Click "Add to table", then "Update", then "Save".
3. Reload and confirm each scope is listed.

## 4. OAuth client

URL: `.../auth/clients/create?project=PROJECT_ID`

1. Application type: Web application.
2. Name: any label.
3. Authorized redirect URI: `http://localhost:<CALLBACK_PORT>/callback`.
4. Tick "Use this client for an AI-powered agent". The vendor guide says requests are rejected without it, and it may not be changeable later. If it was missed, create a new client.
5. Create. In the confirmation dialog click "Download JSON" **before** closing it, because the secret may not be shown again.
6. The downloaded file lands in the browser tool's output folder, not in the user's Downloads folder. A safety hook may block reading `~/Downloads`.

Read only non-secret fields from the JSON:

```sh
jq '.web | {has_secret:((.client_secret // "")|length>0), client_id, project_id, redirect_uris}' <file>
```

## Troubleshooting

- Requests rejected: check the "AI-powered agent" box on the client.
- Connection problems: ask an administrator to check OAuth log events in the security investigation tool.
- Sign-in repeats roughly hourly: the client is not getting a refresh token (see the risks in `SKILL.md`).
- New settings can take 5 minutes to a few hours to apply.
