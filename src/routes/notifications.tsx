import { useEffect, useState } from "react";

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState<any[]>([]);

  useEffect(() => {
    async function fetchNotifications() {
      const response = await fetch("http://127.0.0.1:8000/api/v1/notifications");
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
