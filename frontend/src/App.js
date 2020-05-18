import React from 'react';
import {BrowserRouter as Router,Switch,Route} from "react-router-dom";
import Inicio from "./Inicio";
function App() {
  return (
    <Router>
    <div>
    <a href="http://localhost:5000/login" >Login con Google</a>

      {/* A <Switch> looks through its children <Route>s and
          renders the first one that matches the current URL. */}
      <Switch>
        <Route path="/inicio">
        <Inicio/>
        </Route>
     
      </Switch>
    </div>
  </Router>  );
}

export default App;
