import type { ApiStatus } from "../types/api";

type ChatShellProps = {
  apiStatus: ApiStatus;
};

const statusCopy: Record<ApiStatus, string> = {
  checking: "Memeriksa koneksi…",
  online: "API lokal terhubung",
  offline: "API lokal belum terhubung",
};

export function ChatShell({ apiStatus }: ChatShellProps) {
  return (
    <main className="chat-shell">
      <header className="chat-header">
        <div>
          <p className="eyebrow">VelX showroom</p>
          <h1>Asisten showroom</h1>
        </div>
        <span
          className={`connection-status connection-status--${apiStatus}`}
          role="status"
        >
          {statusCopy[apiStatus]}
        </span>
      </header>

      <section className="conversation" aria-labelledby="conversation-title">
        <div className="empty-state">
          <p className="empty-state__label">Percakapan baru</p>
          <h2 id="conversation-title">Apa yang ingin Anda ketahui?</h2>
          <p>
            Tanyakan tentang showroom, kendaraan, atau langkah berikutnya. Chat
            foundation akan hadir di sini.
          </p>
        </div>
      </section>

      <form className="composer" onSubmit={(event) => event.preventDefault()}>
        <label htmlFor="message">Pesan</label>
        <div className="composer__row">
          <textarea
            id="message"
            name="message"
            placeholder="Tulis pertanyaan Anda…"
            rows={2}
          />
          <button type="submit">Kirim</button>
        </div>
      </form>
    </main>
  );
}
