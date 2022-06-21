import { FunctionalComponent, h } from 'preact';
import { Link } from 'preact-router/match';
import style from './style.css';

const Header: FunctionalComponent = () => {
    return (
        <header class={style.header}>
            <a href ='/'>
                <img src="../../assets/DogeTTM.png"/>
                <h1>DogeTTM <sup>®</sup></h1>
            </a>

            <nav>
                <Link activeClassName={style.active} href="/">
                    Home
                </Link>
                <Link activeClassName={style.active} href="/profile">
                    Me
                </Link>
                <Link activeClassName={style.active} href="/profile/john">
                    John
                </Link>
            </nav>
        </header>
    );
};

export default Header;
