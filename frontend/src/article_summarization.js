import React, {useState} from 'react';
import PropTypes from 'prop-types';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Tooltip from '@material-ui/core/Tooltip';
import IconButton from '@material-ui/core/IconButton';
import { withStyles } from '@material-ui/core/styles';
import SearchIcon from '@material-ui/icons/Search';
import RefreshIcon from '@material-ui/icons/Refresh';
import Slider from '@material-ui/core/Slider';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import Divider from '@material-ui/core/Divider';
import InputLabel from '@material-ui/core/InputLabel';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import NativeSelect from '@material-ui/core/NativeSelect';
import HelpIcon from '@material-ui/icons/Help';
import Backdrop from '@material-ui/core/Backdrop';
import CircularProgress from '@material-ui/core/CircularProgress';
import fetchIntercept from 'fetch-intercept';


const styles = (theme) => ({
  paperPrimary: {
    maxWidth: 3000,
    margin: theme.spacing(1),
    overflow: 'hidden',
  },
  paperSecondary: {
    maxWidth: 300,
    margin: 'auto',
    overflow: 'hidden',
  },
  generateBar: {
    borderBottom: '1px solid rgba(0, 0, 0, 0.12)',
  },
  generateInput: {
    fontSize: theme.typography.fontSize,
  },
  block: {
    display: 'block',
  },
  button: {
    marginRight: theme.spacing(1),
  },
  contentWrapper: {
    margin: '10px 16px',
  },
  slide:{
    width : 200
  },
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  backdrop: {
    zIndex: theme.zIndex.drawer + 1,
    color: '#fff',
  },
});

const apiURL = "http://localhost:8888";

function Article_summarization(props) {
  const { classes } = props;
  let [model, setModel] = useState('korean');
  let [Text, setText] = useState('');
  let [keyword, setKeyword] = useState([]);
  let [summaries, setSummaries] = useState('');
  let [temperature, setTemp] = useState(1.0);
  let [top_p, setTopp] = useState(0.9);
  let [top_k, setTopk] = useState(40);
  let [state, setState] = useState(false);
  
  function _post(Data) {
    const raw = JSON.stringify(Data);

    const requestOptions = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
      },
      body: raw
    };
    fetch(`${apiURL}/api/article-summarization`, requestOptions)
      .then(response =>response.json())
      .then(json => setSummaries(json['summary']))
      .catch(error => setText(error));
      unregister();
  }
  const unregister = fetchIntercept.register({
    request: function (url, config) {
        setState(true);
        return [url, config];
    },

    requestError: function (error) {
      setState(false);
        return Promise.reject(error);
    },

    response: function (response) {
      setState(false);
        return response;
    },

    responseError: function (error) {
      setState(false);
        return Promise.reject(error);
    }
});
  function refresh() {
    setText('');
    setKeyword(['', '', ''])
  }


  function handleClick() {
    const Data = {
      textID: "QuestionGeneration",
      content: Text,
      model: model,
      temperature: temperature,
      top_p: top_p,
      top_k: top_k,
      keywords: keyword,
      sentence_length: "10",
      sentence_count: "3"
    }
    setState(true);
    _post(Data);
  }

  const handleModel = (event) => {
    setModel(event.target.value);
  };
  
  const handleChange = (event) => {
    setText(event.target.value);
  }
  

  function tempSlide(event, newValue) {
    setTemp(newValue);
  }

  function toppSlide(event, newValue) {
    setTopp(newValue);
  }

  function topkSlide(event, newValue) {
    setTopk(newValue);
  }

  return (
    <div>
      <Toolbar>
        <FormControl className={classes.formControl}>
          <InputLabel shrink htmlFor="model selection">
            모델
          </InputLabel>
          <NativeSelect
            onChange={handleModel}
            inputProps={{
            name: 'models',
            id: 'model selection',
            }}>
            <option value="korean">국립국어원 말뭉치</option>
          </NativeSelect>
          {/* <FormHelperText>Label + placeholder</FormHelperText> */}
        </FormControl>
        <span>&nbsp;&nbsp;&nbsp;</span>
        <FormControl className={classes.formControl}>
          <InputLabel shrink htmlFor="example selection">
            예시
          </InputLabel>
          <NativeSelect
            inputProps={{
              name: 'examples',
              id: 'example selection',
            }}>
            <option value="">None</option>
          </NativeSelect>
          {/* <FormHelperText>Label + placeholder</FormHelperText> */}
        </FormControl>
      </Toolbar>
      <Grid container spacing={2}  alignItems="center">
        <Grid item xs={8}>

          <p></p>
          <InputLabel shrink htmlFor="context input">
            본문
          </InputLabel>
          <Paper className={classes.paperPrimary}>
            <Toolbar>
              <Grid container spacing={2}  alignItems="center">
                <Grid item xs>
                  <TextField
                    fullWidth
                    multiline
                    rows={10}
                    placeholder='본문을 입력해주세요.'
                    value={Text}
                    onChange={handleChange}
                    InputProps={{
                      disableUnderline: true,
                      className: classes.searchInput,
                    }}
                  />
                </Grid>
                <Grid item>
                  <Button onClick={handleClick} variant="contained" color="primary" className={classes.button}>
                    생성
                  </Button>
                  <Tooltip title="Refresh">
                    <IconButton onClick={refresh}>
                      <RefreshIcon className={classes.block} color="inherit" />
                    </IconButton>
                  </Tooltip>
                </Grid>
              </Grid>
            </Toolbar>
          </Paper>
          <p></p>
          <InputLabel shrink htmlFor="generation output">
            결과
          </InputLabel>
          <Paper className={classes.paperPrimary}>
            <div className={classes.contentWrapper}>
                <Grid container spacing={2}  alignItems="center">
                    <Typography color="textSecondary" align="center" display = 'block'>
                      {summaries}
                    </Typography>
                </Grid>
            </div>
          </Paper>
        </Grid>

        <Grid item xs>
          <Paper className={classes.paperSecondary} align ='center'>
                <Toolbar alignItems="center">
                    <Grid item xs = {11}>
                        <Typography id="temperature" gutterBottom>
                            temperature : {temperature} 
                        </Typography> 
                    </Grid>
                    <Grid item xs = {1}>
                        <Tooltip title="생성되는 글의 창의성을 조절하는 값입니다.">
                            <IconButton size = 'small' color="inherit">
                                <HelpIcon />
                            </IconButton>
                        </Tooltip>
                    </Grid>
                </Toolbar>
            <Slider
              className={classes.slide}
              defaultValue={1.0}
              aria-labelledby="discrete-slider-small-steps"
              step={0.1}
              marks
              min={0.5}
              max={2.0}
              valueLabelDisplay="auto"
              onChange = {tempSlide}
            />
            <Toolbar alignItems="center">
                    <Grid item xs = {11}>
                    <Typography id="top_p" gutterBottom>
                    top_p : {top_p}
                    </Typography> 
                    </Grid>
                    <Grid item xs = {1}>
                        <Tooltip title="샘플링된 단어 중 top_p 확률 이상의 단어만 선택합니다.">
                            <IconButton size = 'small' color="inherit">
                                <HelpIcon />
                            </IconButton>
                        </Tooltip>
                    </Grid>
                </Toolbar>
            
            <Slider
              className={classes.slide}
              defaultValue={0.9}
              aria-labelledby="discrete-slider-small-steps"
              step={0.05}
              marks
              min={0.5}
              max={1.0}
              valueLabelDisplay="auto"
              onChange = {toppSlide}
            />
            <Toolbar alignItems="center">
                    <Grid item xs = {11}>
                    <Typography id="top_k" gutterBottom>
                      top_k : {top_k}
                    </Typography> 
                    </Grid>
                    <Grid item xs = {1}>
                        <Tooltip title="샘플링된 단어 중 상위 k개의 단어만 선택합니다.">
                            <IconButton size = 'small' color="inherit">
                                <HelpIcon />
                            </IconButton>
                        </Tooltip>
                    </Grid>
                </Toolbar>
            <Slider
              className={classes.slide}
              defaultValue={10}
              aria-labelledby="discrete-slider-small-steps"
              step={5}
              marks
              min={5}
              max={100}
              valueLabelDisplay="auto"
              onChange = {topkSlide}
            />
          </Paper>
        </Grid>
      </Grid>
      <Backdrop className={classes.backdrop} open={state}>
        <CircularProgress color="inherit" />
      </Backdrop>
    </div>
  );
}

Article_summarization.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Article_summarization);