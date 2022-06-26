import { FunctionalComponent, h } from 'preact';
import Ranking from '../../components/Dashboards/Ranking';
import Searchbar from '../../components/Searchbar';
import Sentiment from '../../components/Dashboards/Sentiment';
import style from './style.css';

const Home: FunctionalComponent = () => {
    return (
        <div class={style.home}>
            <Searchbar />
            <div class={style.container}>
                <div class="container-left">
                    <Ranking />
                </div>
                <div class="container-right">
                    <Sentiment />
                </div>
            </div>
        </div>
    );
};

export default Home;
