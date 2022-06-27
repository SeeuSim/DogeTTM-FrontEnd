import { useNft } from 'use-nft';
import { FunctionalComponent, h } from "preact";
import style from './style.css';

interface Props {
    address:string,
    tokens:string
}

const NftImage:FunctionalComponent<Props> = (props:Props) => {
    const {address, tokens} = props
    const randToken = Math.floor(Math.random() * parseInt(tokens));
    const {loading, error, nft} = useNft(
        address, randToken.toString()
    );
    if (loading) return <h1>Loading…</h1>

  // nft.error is an Error instance in case of error.
    if (error || !nft) return <h1>Error.</h1>

    return (
        <img class={style.TableImg} src={nft.image} alt=""></img>
    );
}

export default NftImage;
