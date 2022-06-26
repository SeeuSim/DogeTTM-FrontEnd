import { FunctionalComponent, h } from 'preact';
import { Link } from 'preact-router/match';
import style from './style.css';

const Header: FunctionalComponent = () => {
    return (
        <header class={style.header}>
            <a href="/">
                <h1>
                    <img class={style.logo} src="../../assets/DogeTTM.png"></img>
                    DogeTTM<sup>®</sup>
                </h1>
            </a>
            <nav>
                <Link activeClassName={style.active} href="/">
                    Home
                </Link>
                <Link activeClassName={style.active} href="/profile/token">
                    Token
                </Link>
            </nav>
        </header>
    );
};

export default Header;
