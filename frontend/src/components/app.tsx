
import { FunctionalComponent, h } from 'preact';
import { Route, Router } from 'preact-router';

import Collection from '../routes/collection'
import Home from '../routes/home';
import Profile from '../routes/profile';
import NotFoundPage from '../routes/notfound';
import Header from './header';
import { getDefaultProvider } from "ethers";
import { NftProvider } from "use-nft";
import * as URLCONFIG from "../../URLCONF.json"

const ETHERSCAN_KEY = URLCONFIG.ETHERSCAN;
// ETH mainnet alias under this package is "homestead"
const ethersConfig = {
    provider: getDefaultProvider("homestead", {etherscan:ETHERSCAN_KEY}),
};

const App: FunctionalComponent = () => {
    return (
        <NftProvider fetcher={["ethers", ethersConfig]}>
            <div id="preact_root">
                <Header />
                <Router>
                    <Route path="/" component={Home} />
                    <Route path="/profile/" component={Profile} user="me" />
                    <Route path="/profile/:user" component={Profile} />
                    <Route path="/collections/:contract_address" component={Collection} />
                    <NotFoundPage default />
                </Router>
            </div>
        </NftProvider>
    );
};

export default App;
