import React, {useState} from 'react';
import PropTypes from 'prop-types';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Tooltip from '@material-ui/core/Tooltip';
import IconButton from '@material-ui/core/IconButton';
import { withStyles } from '@material-ui/core/styles';
import RefreshIcon from '@material-ui/icons/Refresh';
import Slider from '@material-ui/core/Slider';
import InputLabel from '@material-ui/core/InputLabel';
import FormControl from '@material-ui/core/FormControl';
import FormHelperText from '@material-ui/core/FormHelperText';
import Select from '@material-ui/core/Select';
import HelpIcon from '@material-ui/icons/Help';
import Backdrop from '@material-ui/core/Backdrop';
import CircularProgress from '@material-ui/core/CircularProgress';
import FetchIntercept from 'fetch-intercept';

// const apiURL = "http://localhost:9999";

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

function Article_summarization(props) {
  const { classes } = props;
  let [model, setModel] = useState('korean');
  let [text, setText] = useState('');
  let [keyword, setKeyword] = useState([]);
  let [summaries, setSummaries] = useState('');
  let [actualSummaries, setActualSummaries] = useState('');
  let [sentenceLength, setSentenceLength] = useState(50);
  let [temperature, setTemperature] = useState(1.0);
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

    fetch(`/api/article-summarization`, requestOptions)
      .then(response =>response.json())
      .then(json => setSummaries(json['summary']))
      .catch(error => setText(error));
      unregister();
  }
  
  const unregister = FetchIntercept.register({
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
      textID: "ArticleSummarization",
      content: text,
      model: model,
      temperature: temperature,
      top_p: top_p,
      top_k: top_k,
      keywords: keyword,
      sentence_length: sentenceLength
    }
    setState(true);
    _post(Data);
  }

  const handleModel = (event) => {
    setModel(event.target.value);
  };

  const handleExample = (event) => {
    const Data = {
      textID: "ArticleSummarization",
      index: event.target.value
    }
    setState(true);

    if (event.target.value === 0) return;

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

    fetch(`/api/get-example`, requestOptions)
      .then(response =>response.json())
      .then(json => setText(json['content'], setActualSummaries(json['summary'])))
      .catch(error => setText(error));
      unregister();
  };
  
  const handleChange = (event) => {
    setText(event.target.value);
  }

  function tempSlide(event, newValue) {
    setTemperature(newValue);
  }

  function toppSlide(event, newValue) {
    setTopp(newValue);
  }

  function topkSlide(event, newValue) {
    setTopk(newValue);
  }
  
  function sentenceLengthSlide(event, newValue) {
    setSentenceLength(newValue);
  }

  return (
    <div>
      <Toolbar>
        <FormControl variant="outlined" className={classes.formControl}>
          <InputLabel shrink htmlFor="model selection">
            모델
          </InputLabel>
          <Select
            native
            onChange={handleModel}
            label="Model"
            inputProps={{
              name: 'models',
              id: 'model selection',
            }}>
            <option value="korean">국립국어원 말뭉치</option>
          </Select>
        </FormControl>
        <FormControl variant="outlined" className={classes.formControl}>
          <InputLabel shrink htmlFor="example selection">
            예시
          </InputLabel>
          <Select
            native
            onChange={handleExample}
            label="Example"
            inputProps={{
              name: 'examples',
              id: 'example selection',
            }}>
            <option value={0}>없음</option>
            <option value={1}>예시 1</option>
            <option value={2}>예시 2</option>
            <option value={3}>예시 3</option>
          </Select>
        </FormControl>
        <span>&nbsp;&nbsp;&nbsp;</span>
        <FormControl variant="outlined" className={classes.formControl}>
          <FormHelperText>문장길이 = {sentenceLength}</FormHelperText>
          <Slider
            className={classes.slide}
            defaultValue={150}
            aria-labelledby="discrete-slider-small-steps"
            step={10}
            marks
            min={50}
            max={250}
            valueLabelDisplay="auto"
            onChange={sentenceLengthSlide}
          />
        </FormControl>
      </Toolbar>
      <p></p>
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
                    value={text}
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
            생성 결과
          </InputLabel>
          <Paper className={classes.paperPrimary}>
            <Toolbar>
              <div className={classes.contentWrapper}>
                  <Grid container spacing={2}  alignItems="center">
                      <Typography color="textSecondary" align="center" display = 'block'>
                        {summaries}
                      </Typography>
                  </Grid>
              </div>
            </Toolbar>
          </Paper>
          <p></p>
          <InputLabel shrink htmlFor="generation golden output">
            실제 요약
          </InputLabel>
          <Paper className={classes.paperPrimary}>
            <Toolbar>
              <div className={classes.contentWrapper}>
                  <Grid container spacing={2}  alignItems="center">
                      <Typography color="textSecondary" align="center" display = 'block'>
                        {actualSummaries}
                      </Typography>
                  </Grid>
              </div>
            </Toolbar>
          </Paper>
        </Grid>

        <Grid item xs>
          <Paper className={classes.paperSecondary} align ='center'>
            <Toolbar alignItems="center">
              <Grid item xs = {11}>
                <Typography id="temperature" gutterBottom>
                    Temperature = {temperature} 
                </Typography> 
              </Grid>
              <Grid item xs = {1}>
                <Tooltip title={<h2>생성되는 글의 창의성을 조절합니다</h2>}>
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
                  Top P = {top_p}
                </Typography> 
              </Grid>
              <Grid item xs = {1}>
                <Tooltip title={<h2>샘플링될 단어의 누적분포 합이 P보다 크지 않도록 제한합니다</h2>}>
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
                  Top K = {top_k}
                </Typography> 
              </Grid>
              <Grid item xs = {1}>
                <Tooltip title={<h2>샘플링될 단어의 갯수를 K개로 제한합니다</h2>}>
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