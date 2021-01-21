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
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import Divider from '@material-ui/core/Divider';
import InputLabel from '@material-ui/core/InputLabel';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import HelpIcon from '@material-ui/icons/Help';
import Backdrop from '@material-ui/core/Backdrop';
import CircularProgress from '@material-ui/core/CircularProgress';
import FetchIntercept from 'fetch-intercept';

//const apiURL = "http://14.49.45.139:9999";

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
  buttons: {
    minWidth: 200,
  },
  backdrop: {
    zIndex: theme.zIndex.drawer + 1,
    color: '#fff',
  },
});

function Question_generation(props) {
  const { classes } = props;
  let [model, setModel] = useState('korquad');
  let [text, setText] = useState('');
  let [keyword, setKeyword] = useState([]);
  let [question, setQuestion] = useState([]);
  let [answer, setAnswer] = useState([]);
  let [temperature, setTemperature] = useState(1.0);
  let [top_p, setTopp] = useState(0.9);
  let [top_k, setTopk] = useState(40);
  let [state, setState] = useState(false);
  let [time, setTime] = useState();
  let [sent, setSent] = useState(false);
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
    fetch(`/api/question-generation`, requestOptions)
      .then(response => response.json())
      .then(json => {
        setQuestion(json['questions'], setAnswer(json['answers']));
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
    setKeyword([])
    setSent(false);
  }

  function handleClick() {
    const Data = {
      textID: "QuestionGeneration",
      content: text,
      model: model,
      temperature: temperature,
      top_p: top_p,
      top_k: top_k,
      keywords: keyword,
      sentence_length: "10"
    }
    setState(true);
    _post(Data);
  }

  const handleModel = (event) => {
    setModel(event.target.value);
  };

  const handleExample = (event) => {
    const Data = {
      textID: "QuestionGeneration",
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
      .then(json => setText(json['content'], setKeyword(json['keyword'])))
      .then()
      .catch(error => setText(error));
      unregister();
  };
  
  const handleChange = (event) => {
    setText(event.target.value);
  }
  
  const handleKeyword = (event) => {
    const arr = event.target.value.replace(' ', '').split(',')
    setKeyword(arr);
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
            <option value="korquad">Korquad v1.0</option>
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
            <option value={1}>코로나 대응</option>
            <option value={2}>도깨비 마을</option>
            <option value={3}>해바라기</option>
          </Select>
        </FormControl>
        <span>&nbsp;&nbsp;&nbsp;</span>
      </Toolbar>
      <Grid container spacing={2}  alignItems="center">
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
                placeholder='본문을 입력해주세요.'
                value={text}
                onChange={handleChange}
                InputProps={{
                  disableUnderline: true,
                  className: classes.searchInput,
                }}
              />
            </Toolbar>
          </Paper>
          <Toolbar>
          <InputLabel shrink htmlFor="keyword input">
            키워드
          </InputLabel>
          </Toolbar>
          <Paper className={classes.paperPrimary}>
            <Toolbar>
              <Grid container spacing={2}  alignItems="center">
                <Grid item xs>
                  <TextField
                    fullWidth
                    placeholder='키워드를 반점으로 나누어 입력해주세요.'
                    onChange={handleKeyword}
                    value={keyword.join()}
                    InputProps={{
                      disableUnderline: true,
                      className: classes.searchInput,
                    }}
                  />
                </Grid>
              </Grid>
            </Toolbar>
          </Paper>
          <div style = {{float:'right'}}>
            <Toolbar>
              <Typography color = "textSecondary">
                {sent ? `응답시간 : ${time}s` : ''}
              </Typography>
              <span>&nbsp;&nbsp;&nbsp;</span>
              <Button onClick={handleClick} variant="contained" color="primary" className={classes.button}>
                질문생성
              </Button>
              <Tooltip title="Refresh">
                <IconButton onClick={refresh}>
                  <RefreshIcon className={classes.block} color="inherit" />
                </IconButton>
              </Tooltip>
            </Toolbar>
          </div>
          <p />
          <Toolbar>
            <InputLabel shrink htmlFor="generation output">
              결과
            </InputLabel>
          </Toolbar>
          <Paper className={classes.paperPrimary}>
            <Toolbar>
              <List>
                {question.map((item, index) => (
                  <ListItem alignItems="flex-start">
                    <ListItemText>
                      {index}. 
                    </ListItemText>
                    <ListItemText>
                      질문: {question[index]}
                    </ListItemText>
                    <Divider variant="inset" component="li" />
                    <ListItemText>
                      정답: {answer[index]}
                    </ListItemText>
                  </ListItem>
                ))}
              </List>
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

Question_generation.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Question_generation);