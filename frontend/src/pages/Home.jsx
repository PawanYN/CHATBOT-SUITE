function Home() {
  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <div className="max-w-4xl w-full bg-white shadow-lg rounded-2xl p-8 md:p-16 text-center">
        <h1 className="text-3xl font-bold mb-4 text-gray-900">Welcome to Chatbot Suite</h1>

        <p className="text-gray-700 mb-4">
          Our chatbot platform helps users communicate with intelligent assistants in a seamless and
          friendly way.
        </p>

        <p className="text-gray-600 mb-6">
          This app is built with React, Tailwind CSS, and FastAPI to deliver modern, fast, and scalable solutions.
        </p>

        <a
          href="/chat"
          className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded"
        >
          Start Chatting
        </a>
      </div>
    </div>
  );
}

export default Home;
