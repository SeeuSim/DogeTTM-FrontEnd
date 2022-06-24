import { FunctionalComponent, h } from 'preact';
import Searchbar from '../../components/searchbar/index';
import Dashboard_Ranking from '../../components/dashboard-ranking/index';
import Dashboard_Sentiment from '../../components/dashboard-sentiment/index';
import style from './style.css';

const Home: FunctionalComponent = () => {
    return (
        <div class={style.home}>
            {/* <h1>Home</h1>
            <p>This is the Home component.</p> */}
            <Searchbar />
            <div class="main-container">
                <div class="main-child left">
                    <Dashboard_Ranking />
                </div>
                <div class="main-child right">
                    <Dashboard_Sentiment />
                </div>
            </div>
        </div>
    );
};

export default Home;
