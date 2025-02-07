import { PageLoadingIcon } from './Loading';
import classes from './PageLoading.module.css';

export const PageLoading = () => {
  return (
    <div className={classes.pageLoaderContainer}>
      <PageLoadingIcon />
    </div>
  );
};
