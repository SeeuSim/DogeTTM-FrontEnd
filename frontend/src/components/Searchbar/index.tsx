import { FunctionalComponent, h } from "preact";
import { useState, useRef, useEffect, useCallback } from "preact/hooks";
import { Link } from "preact-router/match";
import axios from 'axios';
import * as URLCONF from "../../../URLCONF.json";
import style from "style.css";

const baseURL = URLCONF.BACKEND;

type SearchResult = {
  data: SearchResultEntry[]
}

type SearchResultEntry = {
  name: string,
  address: string,
  artwork: string
}

const Searchbar:FunctionalComponent = () => {
  const [options, setOptions] = useState<SearchResultEntry[]>([]);
  const [input, setInput] = useState("");
  const [searchBy, setSearchBy] = useState("name");

  // TODO: Add Data Fetching function and useEffect Hooks

  const fetchData = useCallback(() => {
    axios.get<SearchResult>(`${baseURL}/nft/search/${searchBy}/${input}`)
      .then((res) => setOptions(res.data.data));
  }, [input]);

  useEffect(() => {
    if (input) {
      fetchData();
    }
  }, [input])

  const onInputChange = (e: any) => {
    setInput(e.target.value);
    console.log(input);
  }

  // TODO: Map API Data from backend to a displayable format
  
  const ulRef = useRef<HTMLUListElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.addEventListener('click', (event:any) => {
      event.stopPropagation();
      if (ulRef.current) {
        ulRef.current.style.display = 'flex';
      }
      onInputChange(event);
    });
    document.addEventListener('click', (event:any) => {
      if (ulRef.current) {
        ulRef.current.style.display = 'none';
      }
    });
  }, []);

  return (
    <div>
      <input
        id="search-bar"
        type="text"
        className="form-control"
        placeholder={`Search NFT by `}
        ref={inputRef}
        onChange={(e:any) => onInputChange(e)}
      />
      <ul
        id="results"
        className="list-group"
        ref={ulRef}>
          {options?.map((option:SearchResultEntry, index:Number) => {
            return (
              <button
                type="button"
                key={index}
                className="list-group-item list-group-item-action"
                onClick={(e:any) => {
                  if (inputRef.current) {
                    inputRef.current.value = option.name;
                  }
                }}
                >
                <img src={option.artwork} style="height:56px; width:56px;"></img>
                <Link href={`/collections/${option.address}`}>{option.name}</Link>
              </button>
            );
          })}
      </ul>
    </div>
  )
}


export default Searchbar;
