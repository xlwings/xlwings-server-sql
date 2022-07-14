// TODO: Replace URL with your own URL
const base_url = "URL";
const token = ScriptApp.getOAuthToken();

function selectEmployees() {
  runPython(base_url + "/employees/select", { apiKey: token });
}
