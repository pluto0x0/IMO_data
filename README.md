# IMO_data

Data from <https://artofproblemsolving.com/wiki/index.php/IMO_Problems_and_Solutions>

## Setup

```
pip install -r requirements.txt
```

```
python main.py output_file.json
```

## Data Format

- Problem & Solution in Markdown format (`$ ... $` and `$$ ... $$` for $\LaTeX$ equations, `##` for subtitles) 
- Includes graph URLs
- Arranged in year and Problem No.
- Multiple solutions

### Sample

**(See [data.json](./data.json) for full data)**

```json
{
    "2019": {
            "1": {
                "Problem": {
                    "graphs": [],
                    "text": "Let $\\mathbb{Z}$ be the set of integers. Determine all ..."
                },
                "Solutions": [
                    {
                        "graphs": [],
                        "text": "Let us substitute $0$ in for $a$ to get\n\\[f(0) + 2f(b) = f(f(b)).\\]\nNow, since the domain  ..."
                    },
                    {
                        "graphs": [],
                        "text": "We plug in $a=-b=x$ and $a=-b=x+k$ to get \n\\[f(2x)+2f(-x)=f(f(0)),\\]\n\\[f(2(x+k))+2f(-(x+k))=f(f(0)),\\]\nrespectively.\nSettin ..."
                    },
                    {
                        "graphs": [],
                        "text": "The only solutions are $f(x)=0, 2x+c.$ For some integer $c.$\nObviously these work. ..."
                    },
                    {
                        "graphs": [],
                        "text": "We claim the only solutions are $f\\equiv0$ and $f(x)=2x+c$ for some integer $c$.,  ..."
                    }
                ]
            },
            "2": {
                ...
            },
            ...
    }
    ...
}
```