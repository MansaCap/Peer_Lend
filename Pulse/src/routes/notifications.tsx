import { useEffect, useState } from "react";

const API_BASE_URL = "http://127.0.0.1:8001/api/v1";

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState<any[]>([]);

  useEffect(() => {
    async function fetchNotifications() {
      const response = await fetch(`${API_BASE_URL}/notifications`);
      const data = await response.json();
      setNotifications(data);
    }
    fetchNotifications();
  }, []);

  return (
    <div>
      <h1>Notifications</h1>
      {notifications.length === 0 ? (
        <p>No notifications yet.</p>
      ) : (
        <ul>
          {notifications.map((note, idx) => (
            <li key={idx}>
              <strong>{note.type}</strong>: {note.message} ({note.timestamp})
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
