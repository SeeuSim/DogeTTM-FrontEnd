import { FunctionalComponent, h } from "preact";
import { useState, useRef, useEffect } from "preact/hooks";

const Searchbar:FunctionalComponent = () => {
  const [options, setOptions] = useState<String[]>([]);

  // TODO: Add Data Fetching function and useEffect Hooks

  // TODO: Map API Data from backend to a displayable format
  
  const ulRef = useRef<HTMLUListElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.addEventListener('click', (event:any) => {
      event.stopPropagation();
      if (ulRef.current) {
        ulRef.current.style.display = 'flex';
      }
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
      />
      <ul
        id="results"
        className="list-group"
        ref={ulRef}>
      </ul>
    </div>
  )
}


export default Searchbar;
