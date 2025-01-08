import { Badge, Button, Space, Text } from '@mantine/core';
import baseClasses from '../../../shared-components/shared-styles.module.css';
import { ApiError, BirthingPersonService, OpenAPI } from '../../../client';
import { useNavigate } from 'react-router-dom';
import { LabourStatistics } from '../../../shared-components/LabourStatistics/LabourStatistics';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { NotFoundError } from '../../../Errors';
import { ContainerLoadingIcon } from '../../../shared-components/PageLoading/Loading';


export default function Labours() {
  const auth = useAuth();
  const navigate = useNavigate();

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || ""
  }
  
  const queryClient = useQueryClient();

  const registerBirthingPerson = useMutation({
    mutationFn: async () => {
      const response = await BirthingPersonService.registerApiV1BirthingPersonRegisterPost()
      return response.birthing_person
    },
    onSuccess: (birthingPerson) => {
      queryClient.setQueryData(['birthingPerson', auth.user?.profile.sub], birthingPerson)
    },
    onError: (error) => {
      console.error("Error starting labour", error)
    }
  });

  const { isPending, isError, data, error } = useQuery({
    queryKey: ['birthingPerson', auth.user?.profile.sub],
    queryFn: async () => {
        try {
            const response = await BirthingPersonService.getBirthingPersonApiV1BirthingPersonGet();
            return response.birthing_person;
        } catch (err) {
            if (err instanceof ApiError && err.status === 404) {
                throw new NotFoundError();
            }
            throw new Error("Failed to load labour. Please try again later.")
        }
    },
    retry: (failureCount, error) => {
      if (error instanceof NotFoundError) {
        registerBirthingPerson.mutate();
        return false;
      }
      return failureCount < 3;
    },
  });

  if (isPending) {
    return (
      <div className={baseClasses.body}>
        <Text className={baseClasses.text}><ContainerLoadingIcon /></Text>
      </div>
    )
  }

  if (isError) {
    return <Text className={baseClasses.text}>{error.message}</Text>
  }
  
  if (data.labours.length > 0) {
    const labours = data.labours.map((labour) => (
      <div key={labour.id} className={baseClasses.body} >
        <div className={baseClasses.flexRowNoBP}>
          <Text className={baseClasses.text}>{new Date(labour.start_time).toDateString()}</Text>
          <Badge size='lg' pl={40} pr={40} mb={20} variant="light">{labour.current_phase}</Badge>
        </div>
        <LabourStatistics labour={labour} />
        <Space h={"sm"} />
        {(labour.end_time && labour.notes ) && <Text className={baseClasses.text}>Closing Note: {labour.notes}</Text>}
        <div className={baseClasses.flexRowEndNoBP}>
          {!labour.end_time && <Button color="var(--mantine-color-pink-4)" pl={35} pr={35} radius="lg" variant="filled" onClick={() => navigate("/labour")}>Resume</Button>}
        </div>
      </div>
    ));
    return (
        <div className={baseClasses.flexRow}>
          {labours}
        </div>
    )
  } else {
    return (
      <div className={baseClasses.body}>
        <Text className={baseClasses.text}>Current and past labours will show here</Text>
      </div>
    )
  }
}
