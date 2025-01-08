import { MutatingDots } from "react-loader-spinner"
import classes from "./PageLoading.module.css"

export const PageLoadingIcon = () => {
    return (
        <MutatingDots
            visible={true}
            height="100"
            width="100"
            color="#FF8C7A"
            secondaryColor="#FF8C7A"
            radius="12.5"
            ariaLabel="mutating-dots-loading"
            wrapperStyle={{}}
            wrapperClass=""
        />
    )
}

export const ContainerLoadingIcon = () => {
    return (
        <div className={classes.centerLoader}>
        <MutatingDots
            visible={true}
            radius="12.5"
            height="100"
            width="100"
            color="#FF8C7A"
            secondaryColor="#FF8C7A"
            ariaLabel="mutating-dots-loading"
            wrapperStyle={{}}
            wrapperClass=""
        />
        </div>

    )
}