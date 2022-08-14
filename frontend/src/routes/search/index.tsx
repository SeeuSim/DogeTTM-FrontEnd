import axios from 'axios';
import { FunctionalComponent, h } from "preact";
import { useCallback, useEffect, useState } from "preact/hooks";
import { route } from "preact-router";
import * as URLCONFIG from "../../../URLCONF.json";
import style from "./style.css";

const baseURL = URLCONFIG.BACKEND;

type SearchResultProps = {
    metric: string,
    param: string
}

const SearchResults: FunctionalComponent<SearchResultProps> = (props: SearchResultProps) => {
    const {metric, param} = props;
    const [searchResults, setResults] = useState([]);

    const fetchData = useCallback(() => {
        axios.get(`${baseURL}/nft/search/${metric}/${param}`).then(
            (response) => {
                setResults(response.data);
                console.log(response.data);
            }
        )
    }, [])

    useEffect(() => {
        fetchData();
    }, [])


    return <div class={style.search_main}>
        <h1>{metric} {param}</h1></div>;
}

export default SearchResults;
