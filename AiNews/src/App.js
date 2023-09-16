import MainWindow from "./components/MainWindow/MainWindow";
import AddNews from "./components/AddNews/AddNews";
import AddDateset from "./components/AddDateset/AddDateset";
import { BrowserRouter, Routes, Route } from "react-router-dom"

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <div className="nav">
          <p><b>Ai</b>News</p>
        </div>
        <Routes>
          <Route path="/AiNews/" element={<MainWindow />} />
          <Route path="/AiNews/news" element={<AddNews />} />
          <Route path="/AiNews/dataset" element={<AddDateset />} />
          <Route path="*" element={<MainWindow />} />
        </Routes>
      </div>
    </BrowserRouter >
  );
}

export default App;
