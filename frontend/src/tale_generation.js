import React, { useState } from 'react';
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
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import ListSubheader from '@material-ui/core/ListSubheader';
import InputLabel from '@material-ui/core/InputLabel';
import FormControl from '@material-ui/core/FormControl';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormHelperText from '@material-ui/core/FormHelperText';
import Select from '@material-ui/core/Select';
import Switch from '@material-ui/core/Switch';
import HelpIcon from '@material-ui/icons/Help';
import Backdrop from '@material-ui/core/Backdrop';
import CircularProgress from '@material-ui/core/CircularProgress';
import FetchIntercept from 'fetch-intercept';

import CommentIcon from '@material-ui/icons/Comment';

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
    margin: '40px 16px',
  },
  slide: {
    width: 200
  },
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  rec: {
    textAlign: 'center'
  },
  backdrop: {
    zIndex: theme.zIndex.drawer + 1,
    color: '#fff',
  },
});

function Tale_generation(props) {
  const { classes } = props;
  let [model, setModel] = useState('woongjin');
  let [Text, setText] = useState('');
  let [count, setCount] = useState(3);
  let [temperature, setTemperature] = useState(1.3);
  let [top_p, setTopp] = useState(1.0);
  let [top_k, setTopk] = useState(40);
  let [recommend, setRecommend] = useState([
    { word: '', sentence: '', pos: 0 },
    { word: '', sentence: '', pos: 1 },
    { word: '', sentence: '', pos: 2 }
  ]);
  let [checkedRecommend, setCheckedRecommend] = React.useState(true);
  let [checkedAuto, setCheckedAuto] = React.useState(false);
  let [state, setState] = useState(false);
  let [time, setTime] = useState();
  let [sent, setSent] = useState(false);

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

  const toggleRecommendChecked = () => {
    setCheckedRecommend((prev) => !prev);
  };

  const toggleAutoChecked = () => {
    setCheckedAuto((prev) => !prev);
  };

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

    const start = new Date();

    fetch(`/api/tale-generation`, requestOptions)
    .then(response => response.json())
    .then(json => {
      recommendInput(json['sentences'], json['words'])
      setTime(`${(new Date().getTime()-start.getTime())/1000}`)
      setSent(true);
    })
    .catch(error => {
      setText(error);
      setTime(`${(new Date().getTime()-start.getTime())/1000}`)
      setSent(true);
    });
    unregister();
  }

  function refresh() {
    setText('');
    recommendCount(count);
    setSent(false);
  }

  const handleExample = (event) => {
    const Data = {
      textID: "TaleGeneration",
      index: event.target.value
    }
    
    if (event.target.value === 0) return;
    setState(true);
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
      .then(json => setText(json['content']))
      .catch(error => setText(error));
      unregister();
  };

  const handleChange = (event) => {
    setText(event.target.value);
  }

  function handleRecommend(event, index) {
    (checkedRecommend) ?
      setText(Text + ' ' + recommend[index].sentence)
      :
      setText(Text + ' ' + recommend[index].word)
  }

  function handleClick() {
    const Data = {
      textID: "TaleGeneration",
      content: Text,
      model: model,
      temperature: temperature,
      top_p: top_p,
      top_k: top_k,
      recommend_flag: checkedRecommend,
      auto_flag: checkedAuto,
      count: count
    }
    setState(true);
    _post(Data);
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

  const handleModel = (event) => {
    setModel(event.target.value);
  };

  async function handleCount(event) {
    setCount(event.target.value);
    recommendCount(event.target.value);
  };

  function recommendCount(condition) {
    let arr = [];
    for (let i = 0; i < condition; i++) {
      arr = [...arr, { word: ``, sentence: ``, pos: i }];
    }
    setRecommend(arr);
  }

  function recommendInput(sentenceList, wordsList) {
    let arr = [];
    for (let i = 0; i < count; i++) {
      arr = [...arr, { word: wordsList[i], sentence: sentenceList[i], pos: i }];
    }
    setRecommend(arr);
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
            <option value="woongjin">웅진 도서</option>
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
            <option value={0}>None</option>
            <option value={1}>1</option>
            <option value={2}>2</option>
            <option value={3}>3</option>
          </Select>
        </FormControl>
        <FormControl variant="outlined" className={classes.formControl}>
          <InputLabel shrink htmlFor="model selection">
            생성 개수
          </InputLabel>
          <Select
            native
            onChange={handleCount}
            label="Count"
            inputProps={{
              name: 'counts',
              id: 'recommend count',
            }}>
            <option value={3}>3</option>
            <option value={4}>4</option>
            <option value={5}>5</option>
            <option value={6}>6</option>
            <option value={7}>7</option>
          </Select>
        </FormControl>
        <FormControl className={classes.formControl}>
          <FormHelperText>추천형태</FormHelperText>
          <FormControlLabel
            control={<Switch checked={checkedRecommend} onChange={toggleRecommendChecked} color="primary" />}
            label={checkedRecommend ? '문장' : '단어'}
          />

        </FormControl>
        <FormControl className={classes.formControl}>
          <FormHelperText>자동생성</FormHelperText>
          <FormControlLabel
            control={<Switch checked={checkedAuto} onChange={toggleAutoChecked} color="primary" />}
            label={checkedAuto ? 'ON' : 'OFF'}
          />
        </FormControl>
      </Toolbar>
      <p></p>
      <Grid container spacing={2} alignItems="center">
        <Grid item xs={8}>
          <Toolbar>
            <InputLabel shrink htmlFor="context input">
              본문
            </InputLabel>
          </Toolbar>
          <Paper className={classes.paperPrimary}>
            <Toolbar>
              <TextField
                fullWidth
                multiline
                rows={12}
                placeholder='기사를 입력해주세요'
                value={Text}
                onChange={handleChange}
                InputProps={{
                  disableUnderline: true,
                  className: classes.searchInput,
                }}
              />
            </Toolbar>
          </Paper>
          <div style = {{float:'right'}}>
            <Toolbar>
              <Typography color = "textSecondary">
                {sent ? `응답시간 : ${time}s` : ''}
              </Typography>
              <span>&nbsp;&nbsp;&nbsp;</span>
              <Button onClick={handleClick} variant="contained" color="primary" className={classes.button}>
                {checkedAuto ? '자동생성' : (checkedRecommend ? '문장추천' : '단어추천')}
              </Button>
              <Tooltip title="Refresh">
                <IconButton onClick={refresh}>
                  <RefreshIcon className={classes.block} color="inherit" />
                </IconButton>
              </Tooltip>
            </Toolbar>
          </div>
          <Toolbar>
            <InputLabel shrink htmlFor="context input">
              결과
            </InputLabel>
          </Toolbar>
          <Paper className={classes.paperPrimary}>
            <Toolbar>
              <List component="nav">
                <ListSubheader />
                {recommend.map(({ word: Word, sentence: Sentence, pos: Pos }) => (
                  <ListItem
                    value={checkedRecommend ? Sentence : Word}
                    button
                    onClick={(event) => handleRecommend(event, Pos)}
                    index={Pos}>
                    <CommentIcon color="disabled" />
                    &nbsp;
                    <ListItemText
                      align='left'
                    >
                      {checkedRecommend ? Sentence : Word}
                    </ListItemText>
                    <p />
                  </ListItem>
                ))}
              </List>
            </Toolbar>
          </Paper>
        </Grid>
        <Grid item xs>
          <Paper className={classes.paperSecondary} align='center'>
            <Toolbar alignItems="center">
              <Grid item xs={11}>
                <Typography id="temperature" gutterBottom>
                  Temperature = {temperature}
                </Typography>
              </Grid>
              <Grid item xs={1}>
                <Tooltip title={<h2>생성되는 글의 창의성을 조절합니다</h2>}>
                  <IconButton size='small' color="inherit">
                    <HelpIcon />
                  </IconButton>
                </Tooltip>
              </Grid>
            </Toolbar>
            <Slider
              className={classes.slide}
              defaultValue={1.3}
              aria-labelledby="discrete-slider-small-steps"
              step={0.1}
              marks
              min={0.5}
              max={2.0}
              valueLabelDisplay="auto"
              onChange={tempSlide}
            />
            <Toolbar alignItems="center">
              <Grid item xs={11}>
                <Typography id="top_p" gutterBottom>
                  Top P = {top_p}
                </Typography>
              </Grid>
              <Grid item xs={1}>
                <Tooltip title={<h2>샘플링될 단어의 누적분포 합이 P보다 크지 않도록 제한합니다</h2>}>
                  <IconButton size='small' color="inherit">
                    <HelpIcon />
                  </IconButton>
                </Tooltip>
              </Grid>
            </Toolbar>
            <Slider
              className={classes.slide}
              defaultValue={1.0}
              aria-labelledby="discrete-slider-small-steps"
              step={0.05}
              marks
              min={0.5}
              max={1.0}
              valueLabelDisplay="auto"
              onChange={toppSlide}
            />
            <Toolbar alignItems="center">
              <Grid item xs={11}>
                <Typography id="top_k" gutterBottom>
                  Top K = {top_k}
                </Typography>
              </Grid>
              <Grid item xs={1}>
                <Tooltip title={<h2>샘플링될 단어의 갯수를 K개로 제한합니다</h2>}>
                  <IconButton size='small' color="inherit">
                    <HelpIcon />
                  </IconButton>
                </Tooltip>
              </Grid>
            </Toolbar>
            <Slider
              className={classes.slide}
              defaultValue={40}
              aria-labelledby="discrete-slider-small-steps"
              step={5}
              marks
              min={5}
              max={100}
              valueLabelDisplay="auto"
              onChange={topkSlide}
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

Tale_generation.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Tale_generation);