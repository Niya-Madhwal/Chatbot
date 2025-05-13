import gradio as gr
import requests

def chat_with_graph(query):
    query_lower = query.lower().strip()

    try:
        # Fetch users
        users_resp = requests.get("http://127.0.0.1:8000/users")
        if users_resp.status_code != 200:
            return f"⚠️ Error fetching users: {users_resp.text}"

        users = users_resp.json().get("value", [])
        matched_user = None

        # Try matching user by name or email in query
        for user in users:
            name = user.get("displayName", "").lower()
            mail = user.get("mail", "").lower()
            upn = user.get("userPrincipalName", "").lower()

            if name in query_lower or mail in query_lower or upn in query_lower:
                matched_user = user
                break

        if matched_user:
            return (
                f"👤 **User Details**:\n"
                f"- Name: {matched_user.get('displayName')}\n"
                f"- Email: {matched_user.get('mail') or 'N/A'}\n"
                f"- Job Title: {matched_user.get('jobTitle') or 'N/A'}\n"
                f"- Department: {matched_user.get('department') or 'N/A'}\n"
                f"- UPN: {matched_user.get('userPrincipalName') or 'N/A'}\n"
                f"- ID: {matched_user.get('id')}"
            )
        elif "user" in query_lower:
            return "🔍 I couldn’t find a matching user. Try the full name or email."

        elif "device" in query_lower:
            # Fetch device data
            device_resp = requests.get("http://127.0.0.1:8000/devices")
            if device_resp.status_code != 200:
                return f"⚠️ Error fetching devices: {device_resp.text}"
            devices = device_resp.json().get("value", [])
            if not devices:
                return "📱 No devices found."
            device_list = [f"{d.get('deviceName', 'Unknown')} - {d.get('userDisplayName', 'N/A')}" for d in devices]
            return "\n".join(device_list)

        else:
            return "❓ I can help with user or device details. Try asking something like:\n- 'Get me user John Doe'\n- 'Show me all devices'"

    except Exception as e:
        return f"💥 Unexpected error: {str(e)}"

# Run Gradio interface
gr.Interface(fn=chat_with_graph, inputs="text", outputs="text", title="Microsoft Graph ChatBot").launch()
