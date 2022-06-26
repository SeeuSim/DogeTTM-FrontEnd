
import { FunctionalComponent, h } from 'preact';
import { Route, Router } from 'preact-router';

import Collection from '../routes/collection'
import Home from '../routes/home';
import Profile from '../routes/profile';
import NotFoundPage from '../routes/notfound';
import Header from './header';

const App: FunctionalComponent = () => {
    return (
        <div id="preact_root">
            <Header />
            <Router>
                <Route path="/" component={Home} />
                <Route path="/profile/" component={Profile} user="me" />
                <Route path="/profile/:user" component={Profile} />
                <Route path="/collections/:collection" component={Collection} />
                <NotFoundPage default />
            </Router>
        </div>
    );
};

export default App;
